# Built-in imports
from __future__ import annotations  # allow pre-definition use of types
from dataclasses import dataclass
from enum import Enum
from math import ceil
from typing import Type

# Local imports
from . import validators
from .bch_primitives import (
    DUST,
    SATS_PER_BCH,
    SCRIPT_INT_MAX_WHEN_JAVASCRIPT,
    PublicKey,
    Sats,
    ScriptTimestamp,
    UtxoSats,
)
from .fee import (
    aggregate_fee_sats_to_role,
    FeeAgreement,
)
from .javascript import round_half_up
from .oracle import (
    oracle_pubkey_to_unit_class,
    OracleUnit,
    ScriptPriceInOracleUnitsPerBch,
)
from .role import Role


class UnredeemableError(Exception):
    pass


class Side(str, Enum):
    HEDGE = 'Hedge'
    LONG = 'Long'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    @property
    def other_side(self) -> Side:
        # use a lookup to ensure failure with unknown side
        return {Side.HEDGE: Side.LONG, Side.LONG: Side.HEDGE}[self]

    @classmethod
    def from_string(cls, side_string: str) -> Side:
        return {'hedge': cls.HEDGE, 'long': cls.LONG}[side_string.lower()]


class NominalOracleUnitsXSatsPerBch(int):
    def __init__(self, value):
        super().__init__()
        validators.instance(value, int)  # i.e. don't allow silent coercion
        validators.less_equal(self, SCRIPT_INT_MAX_WHEN_JAVASCRIPT)
        validators.greater_equal(self, SATS_PER_BCH)  # equivalent of 1 nominal oracle unit


class LongLeverage(float):
    min_allowed: float = 1.1
    max_allowed: float = 50.0

    def __init__(self, _):
        super().__init__()
        validators.less_equal(self, self.max_allowed * 1.00001)  # some room for floating point error
        validators.greater_equal(self, self.min_allowed * 0.99999)  # some room for floating point error


# TODO: add "forced maturation" to differentiate from normal case in records?
class RedemptionType(str, Enum):
    LIQUIDATION = 'Liquidation'
    MATURATION = 'Maturation'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, redemption_type_string: str) -> RedemptionType:
        return {'liquidation': cls.LIQUIDATION, 'maturation': cls.MATURATION}[redemption_type_string.lower()]


@dataclass(frozen=True)
class ContractProposal:
    """Details of a proposed contract between a maker and taker. Does not include any funding oriented details such as fees."""
    # Time
    start_timestamp: ScriptTimestamp
    maturity_timestamp: ScriptTimestamp

    # Position settings
    nominal_oracleUnits_x_satsPerBch: NominalOracleUnitsXSatsPerBch

    # Start price is not an actual contract parameter, but one of start price, leverage,
    # or separated side inputs are needed in order for the contract to be fully specified.
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    low_liquidation_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    oracle_public_key: PublicKey

    # Relationship between Roles and Sides
    maker_side: Side

    def __post_init__(self):
        # Note: can make validation a switch with unsafe construction if needed
        self.validate()

    ###############
    # Calculated key values used in actual contract creation and execution
    ###############
    @property
    def total_input_sats(self) -> UtxoSats:
        return UtxoSats(ceil(self.nominal_oracleUnits_x_satsPerBch / self.low_liquidation_price_oracleUnits_per_bch))

    @property
    def hedge_input_sats(self) -> UtxoSats:
        # Round gets a potentially slightly more accurate number.
        # The precision to zero-sum comes from defining long position as "everything else needed to cover liquidation".
        return UtxoSats(round_half_up(self.nominal_oracleUnits_x_satsPerBch / self.start_price_oracleUnits_per_bch))

    @property
    def long_input_sats(self) -> UtxoSats:
        return UtxoSats(self.total_input_sats - self.hedge_input_sats)

    @property
    def oracle_unit_cls(self) -> Type[OracleUnit]:
        return oracle_pubkey_to_unit_class[self.oracle_public_key]

    ###############
    # Approximate unit versions of the inputs
    ###############
    @property
    def total_input_oracleUnits(self) -> OracleUnit:
        return self.oracle_unit_cls(self.effective_nominal_oracleUnits)

    @property
    def hedge_input_oracleUnits(self) -> OracleUnit:
        return self.oracle_unit_cls(self.nominal_oracleUnits_x_satsPerBch / SATS_PER_BCH)

    @property
    def long_input_oracleUnits(self) -> OracleUnit:
        return self.oracle_unit_cls(self.long_input_sats.bch * float(self.start_price_oracleUnits_per_bch))

    ###############
    # Reverse calculated effective values from contract perspective
    ###############
    @property
    def duration_seconds(self) -> int:
        return self.maturity_timestamp - self.start_timestamp

    @property
    def effective_nominal_oracleUnits(self) -> OracleUnit:
        return self.oracle_unit_cls(self.nominal_oracleUnits_x_satsPerBch / SATS_PER_BCH)

    @property
    def effective_long_leverage(self) -> LongLeverage:
        return LongLeverage(1 / (1 - self.low_liquidation_price_oracleUnits_per_bch / self.start_price_oracleUnits_per_bch))

    ###############
    # Sided views
    ###############
    @property
    def taker_side(self) -> Side:
        return self.maker_side.other_side

    @property
    def maker_input_sats(self) -> Sats:
        if self.maker_side == Side.HEDGE:
            return self.hedge_input_sats
        return self.long_input_sats

    @property
    def taker_input_sats(self) -> Sats:
        if self.taker_side == Side.HEDGE:
            return self.hedge_input_sats
        return self.long_input_sats

    @property
    def maker_input_oracleUnits(self) -> OracleUnit:
        if self.maker_side == Side.HEDGE:
            return self.hedge_input_oracleUnits
        return self.long_input_oracleUnits

    @property
    def taker_input_oracleUnits(self) -> OracleUnit:
        if self.taker_side == Side.HEDGE:
            return self.hedge_input_oracleUnits
        return self.long_input_oracleUnits

    ###############
    # Constructors
    ###############
    @staticmethod
    def new_from_intent(start_timestamp: ScriptTimestamp,
                        maturity_timestamp: ScriptTimestamp,
                        nominal_oracleUnits: OracleUnit,
                        long_leverage: LongLeverage,
                        start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch,
                        maker_side: Side,
                        ) -> ContractProposal:
        nominal_oracleUnits_x_satsPerBch = NominalOracleUnitsXSatsPerBch(round_half_up(nominal_oracleUnits * SATS_PER_BCH))
        low_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(float(start_price_oracleUnits_per_bch) * (1 - 1 / long_leverage)))
        return ContractProposal(
            start_timestamp=start_timestamp,
            maturity_timestamp=maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=nominal_oracleUnits_x_satsPerBch,
            start_price_oracleUnits_per_bch=start_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=nominal_oracleUnits.public_key,
            maker_side=maker_side,
        )

    def fund(self, fee_agreements: list[FeeAgreement]) -> ContractFunding:
        return ContractFunding(
            base_proposal=self,
            fee_agreements=tuple(fee_agreements),
        )

    def validate(self):
        # Timing
        min_contract_duration_seconds = 60
        if not (self.duration_seconds >= min_contract_duration_seconds):
            raise ValueError(f'contract duration is {self.duration_seconds} s but it must be >= {min_contract_duration_seconds} s')


@dataclass(frozen=True)
class ContractFunding:
    """Funding details and actions, typically derived from a contract proposal."""
    base_proposal: ContractProposal
    fee_agreements: tuple[FeeAgreement, ...]

    @property
    def fee_sats_to_maker(self):
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.MAKER)

    @property
    def fee_sats_to_taker(self):
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.TAKER)

    @property
    def fee_sats_to_hedge(self):
        if self.base_proposal.maker_side == Side.HEDGE:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    @property
    def fee_sats_to_long(self):
        if self.base_proposal.maker_side == Side.LONG:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    ###############
    # Unit value calculations
    ###############
    @property
    def fee_oracleUnits_to_maker(self):
        fee_bch = aggregate_fee_sats_to_role(self.fee_agreements, Role.MAKER).bch
        fee_oracleUnits = self.base_proposal.oracle_unit_cls(fee_bch * float(self.base_proposal.start_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_taker(self):
        fee_bch = aggregate_fee_sats_to_role(self.fee_agreements, Role.TAKER).bch
        fee_oracleUnits = self.base_proposal.oracle_unit_cls(fee_bch * float(self.base_proposal.start_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_hedge(self):
        if self.base_proposal.maker_side == Side.HEDGE:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    @property
    def fee_oracleUnits_to_long(self):
        if self.base_proposal.maker_side == Side.LONG:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    ###############
    # Specialized calculations
    ###############
    def effective_adjusted_price_oracleUnits_per_bch(self, role: Role) -> float:
        # The direction of price adjustment depends on which side is maker/taker.
        # Without context, positive fees will cause the formula to push the price up.
        # However, in context, the higher initial effective price benefits a hedge
        # maker specifically. Therefore, when the maker is long, we need to reverse
        # the direction of the fees so that the benefit always goes to the maker.
        #
        # Unfortunately, the convention of most of the code is "fees to"
        # instead of "fees from" which the original equation was created with.
        # Therefore, there is an extra -1 causing directionality to look reversed:
        direction = 1
        if self.base_proposal.maker_side == Side.HEDGE:
            direction = -1

        # The calculation is not especially intuitive. Here is the breakdown:
        # Naming:
        # nominal units = u
        # fees paid in bch = fP = Σ(fP1...fPm)
        # fees received in bch = fR = Σ(fR1...fRn)
        # original price = pS
        # adjusted price = pA
        #
        # (fP - fR) = u (1/pS - 1/pA)
        # (fP - fR)/u = 1/pS - 1/pA
        # 1/pA = 1/pS - (fP - fR)/u
        # 1/pA = (u - pS(fP - fR)) / (u pS)
        # pA = u pS / (u - pS(fP - fR))

        u = self.base_proposal.effective_nominal_oracleUnits
        pS = float(self.base_proposal.start_price_oracleUnits_per_bch)
        total_fees_to_role_bch = direction * aggregate_fee_sats_to_role(self.fee_agreements, role).bch
        adjusted_price_oracleUnits_per_bch = u * pS / (u - pS * total_fees_to_role_bch)
        return adjusted_price_oracleUnits_per_bch

    ###############
    # Actions
    ###############
    def redeem(self,
               price_timestamp: ScriptTimestamp,
               price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch,
               force_maturity: bool,
               ) -> ContractRedemption:
        """Redeem the contract according to market conditions or raise an unredeemable error for invalid conditions."""
        reached_maturity_time = price_timestamp >= self.base_proposal.maturity_timestamp
        reached_liquidation_price = price_oracleUnits_per_bch <= self.base_proposal.low_liquidation_price_oracleUnits_per_bch
        if reached_maturity_time or force_maturity:
            # Maturation, even in the case of a liquidation price
            return ContractRedemption(
                base_funding=self,
                end_price_timestamp=price_timestamp,
                naive_end_price_oracleUnits_per_bch=price_oracleUnits_per_bch,
                redemption_type=RedemptionType.MATURATION,
            )
        elif reached_liquidation_price:
            # Liquidation
            return ContractRedemption(
                base_funding=self,
                end_price_timestamp=price_timestamp,
                naive_end_price_oracleUnits_per_bch=price_oracleUnits_per_bch,
                redemption_type=RedemptionType.LIQUIDATION,
            )

        # If conditions did not allow for redemption, throw an error
        raise UnredeemableError


@dataclass(frozen=True)
class ContractRedemption:
    """Outcome of a redeemed contract, especially with respect to the two counterparties."""
    base_funding: ContractFunding
    end_price_timestamp: ScriptTimestamp
    naive_end_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    redemption_type: RedemptionType

    @property
    def clamped_end_price_oracleUnits_per_bch(self) -> ScriptPriceInOracleUnitsPerBch:
        return max(self.naive_end_price_oracleUnits_per_bch, self.base_funding.base_proposal.low_liquidation_price_oracleUnits_per_bch)

    @property
    def total_payout_sats(self) -> UtxoSats:
        # Note: This can be different from total input in the case of liquidation where dust protection is pulled in from outside the contract
        return UtxoSats(self.hedge_payout_sats + self.long_payout_sats)

    @property
    def hedge_payout_sats(self) -> UtxoSats:
        # Note that due to dust safety in the contract, the total actual payout can be greater than total inputs.
        # In reality, the extra dust is covered by an amount sitting on the contract that the contract is not aware of.
        # Use divmod (instead of //) to make it crystal clear this represents integer division of the contract.
        unsafe_hedge_payout_sats, _ = divmod(self.base_funding.base_proposal.nominal_oracleUnits_x_satsPerBch, self.clamped_end_price_oracleUnits_per_bch)
        safe_hedge_payout_sats = max(DUST, unsafe_hedge_payout_sats)
        return UtxoSats(safe_hedge_payout_sats)

    @property
    def long_payout_sats(self) -> UtxoSats:
        # Note that due to dust safety in the contract, the total actual payout can be greater than total inputs.
        # In reality, the extra dust is covered by an amount sitting on the contract that the contract is not aware of.
        unsafe_long_payout_sats = self.base_funding.base_proposal.total_input_sats - self.hedge_payout_sats
        safe_long_payout_sats = max(DUST, unsafe_long_payout_sats)
        return UtxoSats(safe_long_payout_sats)

    ###############
    # Approximate unit versions of the outputs
    ###############
    @property
    def total_payout_oracleUnits(self) -> OracleUnit:
        return self.base_funding.base_proposal.oracle_unit_cls(self.total_payout_sats.bch * float(self.clamped_end_price_oracleUnits_per_bch))

    @property
    def hedge_payout_oracleUnits(self) -> OracleUnit:
        return self.base_funding.base_proposal.oracle_unit_cls(self.hedge_payout_sats.bch * float(self.clamped_end_price_oracleUnits_per_bch))

    @property
    def long_payout_oracleUnits(self) -> OracleUnit:
        return self.base_funding.base_proposal.oracle_unit_cls(self.long_payout_sats.bch * float(self.clamped_end_price_oracleUnits_per_bch))

    ###############
    # Gains - see funding class for details of fee and gain calculations
    ###############
    @property
    def hedge_gain_sats(self) -> Sats:
        payout_sats = self.hedge_payout_sats
        input_sats = self.base_funding.base_proposal.hedge_input_sats
        fee_sats = self.base_funding.fee_sats_to_hedge
        return Sats(payout_sats - input_sats + fee_sats)

    @property
    def long_gain_sats(self) -> Sats:
        payout_sats = self.long_payout_sats
        input_sats = self.base_funding.base_proposal.long_input_sats
        fee_sats = self.base_funding.fee_sats_to_long
        return Sats(payout_sats - input_sats + fee_sats)

    ###############
    # Approximate unit versions of the gains
    ###############
    @property
    def hedge_gain_oracleUnits(self) -> OracleUnit:
        # Note that we use naive end price. This represents reality of slippage in liquidations.
        return self.base_funding.base_proposal.oracle_unit_cls(self.hedge_gain_sats.bch * float(self.naive_end_price_oracleUnits_per_bch))

    @property
    def long_gain_oracleUnits(self) -> OracleUnit:
        # Note that we use naive end price. This represents reality of slippage in liquidations.
        return self.base_funding.base_proposal.oracle_unit_cls(self.long_gain_sats.bch * float(self.naive_end_price_oracleUnits_per_bch))

    ###############
    # Relative gains
    ###############
    @property
    def hedge_gain_percent_of_own_input(self) -> float:
        return 100.0 * float(self.hedge_gain_sats) / float(self.base_funding.base_proposal.hedge_input_sats)

    @property
    def long_gain_percent_of_own_input(self) -> float:
        return 100.0 * float(self.long_gain_sats) / float(self.base_funding.base_proposal.long_input_sats)

    ###############
    # Sided views on all of the above
    ###############
    @property
    def maker_payout_sats(self) -> UtxoSats:
        if self.base_funding.base_proposal.maker_side == Side.HEDGE:
            return self.hedge_payout_sats
        return self.long_payout_sats

    @property
    def taker_payout_sats(self) -> UtxoSats:
        if self.base_funding.base_proposal.taker_side == Side.HEDGE:
            return self.hedge_payout_sats
        return self.long_payout_sats

    @property
    def maker_payout_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.HEDGE:
            return self.hedge_payout_oracleUnits
        return self.long_payout_oracleUnits

    @property
    def taker_payout_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.taker_side == Side.HEDGE:
            return self.hedge_payout_oracleUnits
        return self.long_payout_oracleUnits

    @property
    def maker_gain_sats(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.HEDGE:
            return self.hedge_gain_sats
        return self.long_gain_sats

    @property
    def taker_gain_sats(self) -> Sats:
        if self.base_funding.base_proposal.taker_side == Side.HEDGE:
            return self.hedge_gain_sats
        return self.long_gain_sats

    @property
    def maker_gain_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.HEDGE:
            return self.hedge_gain_oracleUnits
        return self.long_gain_oracleUnits

    @property
    def taker_gain_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.taker_side == Side.HEDGE:
            return self.hedge_gain_oracleUnits
        return self.long_gain_oracleUnits

    @property
    def maker_gain_percent_of_own_input(self) -> float:
        if self.base_funding.base_proposal.maker_side == Side.HEDGE:
            return self.hedge_gain_percent_of_own_input
        return self.long_gain_percent_of_own_input

    @property
    def taker_gain_percent_of_own_input(self) -> float:
        if self.base_funding.base_proposal.taker_side == Side.HEDGE:
            return self.hedge_gain_percent_of_own_input
        return self.long_gain_percent_of_own_input
