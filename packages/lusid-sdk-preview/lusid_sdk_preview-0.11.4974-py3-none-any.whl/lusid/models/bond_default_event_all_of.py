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


class BondDefaultEventAllOf(object):
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
        'amount': 'float',
        'coupon_paid_date': 'datetime',
        'default_status': 'str',
        'default_type': 'str',
        'grace_end_date': 'datetime',
        'payment_date': 'datetime',
        'instrument_event_type': 'str'
    }

    attribute_map = {
        'amount': 'amount',
        'coupon_paid_date': 'couponPaidDate',
        'default_status': 'defaultStatus',
        'default_type': 'defaultType',
        'grace_end_date': 'graceEndDate',
        'payment_date': 'paymentDate',
        'instrument_event_type': 'instrumentEventType'
    }

    required_map = {
        'amount': 'required',
        'coupon_paid_date': 'required',
        'default_status': 'required',
        'default_type': 'required',
        'grace_end_date': 'required',
        'payment_date': 'required',
        'instrument_event_type': 'required'
    }

    def __init__(self, amount=None, coupon_paid_date=None, default_status=None, default_type=None, grace_end_date=None, payment_date=None, instrument_event_type=None, local_vars_configuration=None):  # noqa: E501
        """BondDefaultEventAllOf - a model defined in OpenAPI"
        
        :param amount:  Percentage or amount of each share held to be given to shareholders. (required)
        :type amount: float
        :param coupon_paid_date:  Date that the missed coupon is paid if payment is made within grace period. (required)
        :type coupon_paid_date: datetime
        :param default_status:  The status of the bond default (i.e., technical or default)    Supported string (enumeration) values are: [Technical, Default]. (required)
        :type default_status: str
        :param default_type:  The type of the default. (coupon payment, principal payment, covenant ...)    Supported string (enumeration) values are: [CouponPayment, CouponAndPrincipalPayment, PrincipalPayment, Covenant, Bankruptcy, BuyBackOption]. (required)
        :type default_type: str
        :param grace_end_date:  Date the grace period for making coupon payment ends. (required)
        :type grace_end_date: datetime
        :param payment_date:  The date the coupon payment was missed. (required)
        :type payment_date: datetime
        :param instrument_event_type:  The Type of Event. The available values are: TransitionEvent, InternalEvent, CouponEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent (required)
        :type instrument_event_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._amount = None
        self._coupon_paid_date = None
        self._default_status = None
        self._default_type = None
        self._grace_end_date = None
        self._payment_date = None
        self._instrument_event_type = None
        self.discriminator = None

        self.amount = amount
        self.coupon_paid_date = coupon_paid_date
        self.default_status = default_status
        self.default_type = default_type
        self.grace_end_date = grace_end_date
        self.payment_date = payment_date
        self.instrument_event_type = instrument_event_type

    @property
    def amount(self):
        """Gets the amount of this BondDefaultEventAllOf.  # noqa: E501

        Percentage or amount of each share held to be given to shareholders.  # noqa: E501

        :return: The amount of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this BondDefaultEventAllOf.

        Percentage or amount of each share held to be given to shareholders.  # noqa: E501

        :param amount: The amount of this BondDefaultEventAllOf.  # noqa: E501
        :type amount: float
        """
        if self.local_vars_configuration.client_side_validation and amount is None:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def coupon_paid_date(self):
        """Gets the coupon_paid_date of this BondDefaultEventAllOf.  # noqa: E501

        Date that the missed coupon is paid if payment is made within grace period.  # noqa: E501

        :return: The coupon_paid_date of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._coupon_paid_date

    @coupon_paid_date.setter
    def coupon_paid_date(self, coupon_paid_date):
        """Sets the coupon_paid_date of this BondDefaultEventAllOf.

        Date that the missed coupon is paid if payment is made within grace period.  # noqa: E501

        :param coupon_paid_date: The coupon_paid_date of this BondDefaultEventAllOf.  # noqa: E501
        :type coupon_paid_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and coupon_paid_date is None:  # noqa: E501
            raise ValueError("Invalid value for `coupon_paid_date`, must not be `None`")  # noqa: E501

        self._coupon_paid_date = coupon_paid_date

    @property
    def default_status(self):
        """Gets the default_status of this BondDefaultEventAllOf.  # noqa: E501

        The status of the bond default (i.e., technical or default)    Supported string (enumeration) values are: [Technical, Default].  # noqa: E501

        :return: The default_status of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._default_status

    @default_status.setter
    def default_status(self, default_status):
        """Sets the default_status of this BondDefaultEventAllOf.

        The status of the bond default (i.e., technical or default)    Supported string (enumeration) values are: [Technical, Default].  # noqa: E501

        :param default_status: The default_status of this BondDefaultEventAllOf.  # noqa: E501
        :type default_status: str
        """
        if self.local_vars_configuration.client_side_validation and default_status is None:  # noqa: E501
            raise ValueError("Invalid value for `default_status`, must not be `None`")  # noqa: E501

        self._default_status = default_status

    @property
    def default_type(self):
        """Gets the default_type of this BondDefaultEventAllOf.  # noqa: E501

        The type of the default. (coupon payment, principal payment, covenant ...)    Supported string (enumeration) values are: [CouponPayment, CouponAndPrincipalPayment, PrincipalPayment, Covenant, Bankruptcy, BuyBackOption].  # noqa: E501

        :return: The default_type of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._default_type

    @default_type.setter
    def default_type(self, default_type):
        """Sets the default_type of this BondDefaultEventAllOf.

        The type of the default. (coupon payment, principal payment, covenant ...)    Supported string (enumeration) values are: [CouponPayment, CouponAndPrincipalPayment, PrincipalPayment, Covenant, Bankruptcy, BuyBackOption].  # noqa: E501

        :param default_type: The default_type of this BondDefaultEventAllOf.  # noqa: E501
        :type default_type: str
        """
        if self.local_vars_configuration.client_side_validation and default_type is None:  # noqa: E501
            raise ValueError("Invalid value for `default_type`, must not be `None`")  # noqa: E501

        self._default_type = default_type

    @property
    def grace_end_date(self):
        """Gets the grace_end_date of this BondDefaultEventAllOf.  # noqa: E501

        Date the grace period for making coupon payment ends.  # noqa: E501

        :return: The grace_end_date of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._grace_end_date

    @grace_end_date.setter
    def grace_end_date(self, grace_end_date):
        """Sets the grace_end_date of this BondDefaultEventAllOf.

        Date the grace period for making coupon payment ends.  # noqa: E501

        :param grace_end_date: The grace_end_date of this BondDefaultEventAllOf.  # noqa: E501
        :type grace_end_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and grace_end_date is None:  # noqa: E501
            raise ValueError("Invalid value for `grace_end_date`, must not be `None`")  # noqa: E501

        self._grace_end_date = grace_end_date

    @property
    def payment_date(self):
        """Gets the payment_date of this BondDefaultEventAllOf.  # noqa: E501

        The date the coupon payment was missed.  # noqa: E501

        :return: The payment_date of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        """Sets the payment_date of this BondDefaultEventAllOf.

        The date the coupon payment was missed.  # noqa: E501

        :param payment_date: The payment_date of this BondDefaultEventAllOf.  # noqa: E501
        :type payment_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and payment_date is None:  # noqa: E501
            raise ValueError("Invalid value for `payment_date`, must not be `None`")  # noqa: E501

        self._payment_date = payment_date

    @property
    def instrument_event_type(self):
        """Gets the instrument_event_type of this BondDefaultEventAllOf.  # noqa: E501

        The Type of Event. The available values are: TransitionEvent, InternalEvent, CouponEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent  # noqa: E501

        :return: The instrument_event_type of this BondDefaultEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_event_type

    @instrument_event_type.setter
    def instrument_event_type(self, instrument_event_type):
        """Sets the instrument_event_type of this BondDefaultEventAllOf.

        The Type of Event. The available values are: TransitionEvent, InternalEvent, CouponEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent  # noqa: E501

        :param instrument_event_type: The instrument_event_type of this BondDefaultEventAllOf.  # noqa: E501
        :type instrument_event_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_event_type`, must not be `None`")  # noqa: E501
        allowed_values = ["TransitionEvent", "InternalEvent", "CouponEvent", "OpenEvent", "CloseEvent", "StockSplitEvent", "BondDefaultEvent", "CashDividendEvent"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_event_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_event_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_event_type, allowed_values)
            )

        self._instrument_event_type = instrument_event_type

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
        if not isinstance(other, BondDefaultEventAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BondDefaultEventAllOf):
            return True

        return self.to_dict() != other.to_dict()
