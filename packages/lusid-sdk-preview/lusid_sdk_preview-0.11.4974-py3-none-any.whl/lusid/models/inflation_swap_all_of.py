# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.4974
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class InflationSwapAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'start_date': 'datetime',
        'maturity_date': 'datetime',
        'flow_conventions': 'FlowConventions',
        'fixed_rate': 'float',
        'inflation_cap': 'float',
        'inflation_floor': 'float',
        'inflation_frequency': 'str',
        'inflation_index_name': 'str',
        'inflation_interpolation': 'str',
        'inflation_roll_day': 'int',
        'notional': 'float',
        'observation_lag': 'str',
        'pay_receive': 'str',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'maturity_date': 'maturityDate',
        'flow_conventions': 'flowConventions',
        'fixed_rate': 'fixedRate',
        'inflation_cap': 'inflationCap',
        'inflation_floor': 'inflationFloor',
        'inflation_frequency': 'inflationFrequency',
        'inflation_index_name': 'inflationIndexName',
        'inflation_interpolation': 'inflationInterpolation',
        'inflation_roll_day': 'inflationRollDay',
        'notional': 'notional',
        'observation_lag': 'observationLag',
        'pay_receive': 'payReceive',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'maturity_date': 'required',
        'flow_conventions': 'required',
        'fixed_rate': 'required',
        'inflation_cap': 'optional',
        'inflation_floor': 'optional',
        'inflation_frequency': 'optional',
        'inflation_index_name': 'required',
        'inflation_interpolation': 'optional',
        'inflation_roll_day': 'optional',
        'notional': 'required',
        'observation_lag': 'required',
        'pay_receive': 'optional',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, maturity_date=None, flow_conventions=None, fixed_rate=None, inflation_cap=None, inflation_floor=None, inflation_frequency=None, inflation_index_name=None, inflation_interpolation=None, inflation_roll_day=None, notional=None, observation_lag=None, pay_receive=None, instrument_type=None, local_vars_configuration=None):  # noqa: E501
        """InflationSwapAllOf - a model defined in OpenAPI"
        
        :param start_date:  The start date of the instrument. This is normally synonymous with the trade-date. (required)
        :type start_date: datetime
        :param maturity_date:  The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it. (required)
        :type maturity_date: datetime
        :param flow_conventions:  (required)
        :type flow_conventions: lusid.FlowConventions
        :param fixed_rate:  Fixed Rate (required)
        :type fixed_rate: float
        :param inflation_cap:  Optional cap, needed for LPI swaps. Should not be set for ZCIIS.
        :type inflation_cap: float
        :param inflation_floor:  Optional floor, needed for LPI swaps. Should not be set for ZCIIS.
        :type inflation_floor: float
        :param inflation_frequency:  Frequency of inflation updated. Optional and defaults to Monthly which is the most common.  However both Australian and New Zealand inflation is published Quarterly. Only tenors of 1M or 3M are supported.
        :type inflation_frequency: str
        :param inflation_index_name:  Name (required)
        :type inflation_index_name: str
        :param inflation_interpolation:  silly flag for old swaps    Supported string (enumeration) values are: [Linear, Flat].
        :type inflation_interpolation: str
        :param inflation_roll_day:  Day of the month that inflation rolls from one month to the next. This is optional and defaults to 1, which is  the typically value for the majority of inflation bonds (exceptions include Japan which rolls on the 10th  and some LatAm bonds which roll on the 15th).
        :type inflation_roll_day: int
        :param notional:  The notional (required)
        :type notional: float
        :param observation_lag:  Observation Lag, must be a number of Months, typically 3 or 4 but sometimes 8. (required)
        :type observation_lag: str
        :param pay_receive:  PayReceive flag for the inflation leg.  This field is optional and defaults to Pay.  If set to Pay, this swap pays inflation and receives fixed.    Supported string (enumeration) values are: [Pay, Receive].
        :type pay_receive: str
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap (required)
        :type instrument_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._start_date = None
        self._maturity_date = None
        self._flow_conventions = None
        self._fixed_rate = None
        self._inflation_cap = None
        self._inflation_floor = None
        self._inflation_frequency = None
        self._inflation_index_name = None
        self._inflation_interpolation = None
        self._inflation_roll_day = None
        self._notional = None
        self._observation_lag = None
        self._pay_receive = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.maturity_date = maturity_date
        self.flow_conventions = flow_conventions
        self.fixed_rate = fixed_rate
        self.inflation_cap = inflation_cap
        self.inflation_floor = inflation_floor
        self.inflation_frequency = inflation_frequency
        self.inflation_index_name = inflation_index_name
        self.inflation_interpolation = inflation_interpolation
        if inflation_roll_day is not None:
            self.inflation_roll_day = inflation_roll_day
        self.notional = notional
        self.observation_lag = observation_lag
        self.pay_receive = pay_receive
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this InflationSwapAllOf.  # noqa: E501

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :return: The start_date of this InflationSwapAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this InflationSwapAllOf.

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :param start_date: The start_date of this InflationSwapAllOf.  # noqa: E501
        :type start_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_date is None:  # noqa: E501
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def maturity_date(self):
        """Gets the maturity_date of this InflationSwapAllOf.  # noqa: E501

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it.  # noqa: E501

        :return: The maturity_date of this InflationSwapAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self, maturity_date):
        """Sets the maturity_date of this InflationSwapAllOf.

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it.  # noqa: E501

        :param maturity_date: The maturity_date of this InflationSwapAllOf.  # noqa: E501
        :type maturity_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and maturity_date is None:  # noqa: E501
            raise ValueError("Invalid value for `maturity_date`, must not be `None`")  # noqa: E501

        self._maturity_date = maturity_date

    @property
    def flow_conventions(self):
        """Gets the flow_conventions of this InflationSwapAllOf.  # noqa: E501


        :return: The flow_conventions of this InflationSwapAllOf.  # noqa: E501
        :rtype: lusid.FlowConventions
        """
        return self._flow_conventions

    @flow_conventions.setter
    def flow_conventions(self, flow_conventions):
        """Sets the flow_conventions of this InflationSwapAllOf.


        :param flow_conventions: The flow_conventions of this InflationSwapAllOf.  # noqa: E501
        :type flow_conventions: lusid.FlowConventions
        """
        if self.local_vars_configuration.client_side_validation and flow_conventions is None:  # noqa: E501
            raise ValueError("Invalid value for `flow_conventions`, must not be `None`")  # noqa: E501

        self._flow_conventions = flow_conventions

    @property
    def fixed_rate(self):
        """Gets the fixed_rate of this InflationSwapAllOf.  # noqa: E501

        Fixed Rate  # noqa: E501

        :return: The fixed_rate of this InflationSwapAllOf.  # noqa: E501
        :rtype: float
        """
        return self._fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, fixed_rate):
        """Sets the fixed_rate of this InflationSwapAllOf.

        Fixed Rate  # noqa: E501

        :param fixed_rate: The fixed_rate of this InflationSwapAllOf.  # noqa: E501
        :type fixed_rate: float
        """
        if self.local_vars_configuration.client_side_validation and fixed_rate is None:  # noqa: E501
            raise ValueError("Invalid value for `fixed_rate`, must not be `None`")  # noqa: E501

        self._fixed_rate = fixed_rate

    @property
    def inflation_cap(self):
        """Gets the inflation_cap of this InflationSwapAllOf.  # noqa: E501

        Optional cap, needed for LPI swaps. Should not be set for ZCIIS.  # noqa: E501

        :return: The inflation_cap of this InflationSwapAllOf.  # noqa: E501
        :rtype: float
        """
        return self._inflation_cap

    @inflation_cap.setter
    def inflation_cap(self, inflation_cap):
        """Sets the inflation_cap of this InflationSwapAllOf.

        Optional cap, needed for LPI swaps. Should not be set for ZCIIS.  # noqa: E501

        :param inflation_cap: The inflation_cap of this InflationSwapAllOf.  # noqa: E501
        :type inflation_cap: float
        """

        self._inflation_cap = inflation_cap

    @property
    def inflation_floor(self):
        """Gets the inflation_floor of this InflationSwapAllOf.  # noqa: E501

        Optional floor, needed for LPI swaps. Should not be set for ZCIIS.  # noqa: E501

        :return: The inflation_floor of this InflationSwapAllOf.  # noqa: E501
        :rtype: float
        """
        return self._inflation_floor

    @inflation_floor.setter
    def inflation_floor(self, inflation_floor):
        """Sets the inflation_floor of this InflationSwapAllOf.

        Optional floor, needed for LPI swaps. Should not be set for ZCIIS.  # noqa: E501

        :param inflation_floor: The inflation_floor of this InflationSwapAllOf.  # noqa: E501
        :type inflation_floor: float
        """

        self._inflation_floor = inflation_floor

    @property
    def inflation_frequency(self):
        """Gets the inflation_frequency of this InflationSwapAllOf.  # noqa: E501

        Frequency of inflation updated. Optional and defaults to Monthly which is the most common.  However both Australian and New Zealand inflation is published Quarterly. Only tenors of 1M or 3M are supported.  # noqa: E501

        :return: The inflation_frequency of this InflationSwapAllOf.  # noqa: E501
        :rtype: str
        """
        return self._inflation_frequency

    @inflation_frequency.setter
    def inflation_frequency(self, inflation_frequency):
        """Sets the inflation_frequency of this InflationSwapAllOf.

        Frequency of inflation updated. Optional and defaults to Monthly which is the most common.  However both Australian and New Zealand inflation is published Quarterly. Only tenors of 1M or 3M are supported.  # noqa: E501

        :param inflation_frequency: The inflation_frequency of this InflationSwapAllOf.  # noqa: E501
        :type inflation_frequency: str
        """

        self._inflation_frequency = inflation_frequency

    @property
    def inflation_index_name(self):
        """Gets the inflation_index_name of this InflationSwapAllOf.  # noqa: E501

        Name  # noqa: E501

        :return: The inflation_index_name of this InflationSwapAllOf.  # noqa: E501
        :rtype: str
        """
        return self._inflation_index_name

    @inflation_index_name.setter
    def inflation_index_name(self, inflation_index_name):
        """Sets the inflation_index_name of this InflationSwapAllOf.

        Name  # noqa: E501

        :param inflation_index_name: The inflation_index_name of this InflationSwapAllOf.  # noqa: E501
        :type inflation_index_name: str
        """
        if self.local_vars_configuration.client_side_validation and inflation_index_name is None:  # noqa: E501
            raise ValueError("Invalid value for `inflation_index_name`, must not be `None`")  # noqa: E501

        self._inflation_index_name = inflation_index_name

    @property
    def inflation_interpolation(self):
        """Gets the inflation_interpolation of this InflationSwapAllOf.  # noqa: E501

        silly flag for old swaps    Supported string (enumeration) values are: [Linear, Flat].  # noqa: E501

        :return: The inflation_interpolation of this InflationSwapAllOf.  # noqa: E501
        :rtype: str
        """
        return self._inflation_interpolation

    @inflation_interpolation.setter
    def inflation_interpolation(self, inflation_interpolation):
        """Sets the inflation_interpolation of this InflationSwapAllOf.

        silly flag for old swaps    Supported string (enumeration) values are: [Linear, Flat].  # noqa: E501

        :param inflation_interpolation: The inflation_interpolation of this InflationSwapAllOf.  # noqa: E501
        :type inflation_interpolation: str
        """

        self._inflation_interpolation = inflation_interpolation

    @property
    def inflation_roll_day(self):
        """Gets the inflation_roll_day of this InflationSwapAllOf.  # noqa: E501

        Day of the month that inflation rolls from one month to the next. This is optional and defaults to 1, which is  the typically value for the majority of inflation bonds (exceptions include Japan which rolls on the 10th  and some LatAm bonds which roll on the 15th).  # noqa: E501

        :return: The inflation_roll_day of this InflationSwapAllOf.  # noqa: E501
        :rtype: int
        """
        return self._inflation_roll_day

    @inflation_roll_day.setter
    def inflation_roll_day(self, inflation_roll_day):
        """Sets the inflation_roll_day of this InflationSwapAllOf.

        Day of the month that inflation rolls from one month to the next. This is optional and defaults to 1, which is  the typically value for the majority of inflation bonds (exceptions include Japan which rolls on the 10th  and some LatAm bonds which roll on the 15th).  # noqa: E501

        :param inflation_roll_day: The inflation_roll_day of this InflationSwapAllOf.  # noqa: E501
        :type inflation_roll_day: int
        """

        self._inflation_roll_day = inflation_roll_day

    @property
    def notional(self):
        """Gets the notional of this InflationSwapAllOf.  # noqa: E501

        The notional  # noqa: E501

        :return: The notional of this InflationSwapAllOf.  # noqa: E501
        :rtype: float
        """
        return self._notional

    @notional.setter
    def notional(self, notional):
        """Sets the notional of this InflationSwapAllOf.

        The notional  # noqa: E501

        :param notional: The notional of this InflationSwapAllOf.  # noqa: E501
        :type notional: float
        """
        if self.local_vars_configuration.client_side_validation and notional is None:  # noqa: E501
            raise ValueError("Invalid value for `notional`, must not be `None`")  # noqa: E501

        self._notional = notional

    @property
    def observation_lag(self):
        """Gets the observation_lag of this InflationSwapAllOf.  # noqa: E501

        Observation Lag, must be a number of Months, typically 3 or 4 but sometimes 8.  # noqa: E501

        :return: The observation_lag of this InflationSwapAllOf.  # noqa: E501
        :rtype: str
        """
        return self._observation_lag

    @observation_lag.setter
    def observation_lag(self, observation_lag):
        """Sets the observation_lag of this InflationSwapAllOf.

        Observation Lag, must be a number of Months, typically 3 or 4 but sometimes 8.  # noqa: E501

        :param observation_lag: The observation_lag of this InflationSwapAllOf.  # noqa: E501
        :type observation_lag: str
        """
        if self.local_vars_configuration.client_side_validation and observation_lag is None:  # noqa: E501
            raise ValueError("Invalid value for `observation_lag`, must not be `None`")  # noqa: E501

        self._observation_lag = observation_lag

    @property
    def pay_receive(self):
        """Gets the pay_receive of this InflationSwapAllOf.  # noqa: E501

        PayReceive flag for the inflation leg.  This field is optional and defaults to Pay.  If set to Pay, this swap pays inflation and receives fixed.    Supported string (enumeration) values are: [Pay, Receive].  # noqa: E501

        :return: The pay_receive of this InflationSwapAllOf.  # noqa: E501
        :rtype: str
        """
        return self._pay_receive

    @pay_receive.setter
    def pay_receive(self, pay_receive):
        """Sets the pay_receive of this InflationSwapAllOf.

        PayReceive flag for the inflation leg.  This field is optional and defaults to Pay.  If set to Pay, this swap pays inflation and receives fixed.    Supported string (enumeration) values are: [Pay, Receive].  # noqa: E501

        :param pay_receive: The pay_receive of this InflationSwapAllOf.  # noqa: E501
        :type pay_receive: str
        """

        self._pay_receive = pay_receive

    @property
    def instrument_type(self):
        """Gets the instrument_type of this InflationSwapAllOf.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :return: The instrument_type of this InflationSwapAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this InflationSwapAllOf.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :param instrument_type: The instrument_type of this InflationSwapAllOf.  # noqa: E501
        :type instrument_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashFlowsLeg", "Unknown", "TermDeposit", "ContractForDifference", "EquitySwap", "CashPerpetual", "CapFloor", "CashSettled", "CdsIndex", "Basket", "FundingLeg", "FxSwap", "ForwardRateAgreement", "SimpleInstrument", "Repo", "Equity", "ExchangeTradedOption", "ReferenceInstrument", "ComplexBond", "InflationLinkedBond", "InflationSwap"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InflationSwapAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InflationSwapAllOf):
            return True

        return self.to_dict() != other.to_dict()
