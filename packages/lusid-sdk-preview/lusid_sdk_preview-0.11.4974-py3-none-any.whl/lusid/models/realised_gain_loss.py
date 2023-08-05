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


class RealisedGainLoss(object):
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
        'instrument_scope': 'str',
        'instrument_uid': 'str',
        'units': 'float',
        'purchase_trade_date': 'datetime',
        'purchase_settlement_date': 'datetime',
        'purchase_price': 'float',
        'cost_trade_ccy': 'CurrencyAndAmount',
        'cost_portfolio_ccy': 'CurrencyAndAmount',
        'realised_trade_ccy': 'CurrencyAndAmount',
        'realised_total': 'CurrencyAndAmount',
        'realised_market': 'CurrencyAndAmount',
        'realised_currency': 'CurrencyAndAmount'
    }

    attribute_map = {
        'instrument_scope': 'instrumentScope',
        'instrument_uid': 'instrumentUid',
        'units': 'units',
        'purchase_trade_date': 'purchaseTradeDate',
        'purchase_settlement_date': 'purchaseSettlementDate',
        'purchase_price': 'purchasePrice',
        'cost_trade_ccy': 'costTradeCcy',
        'cost_portfolio_ccy': 'costPortfolioCcy',
        'realised_trade_ccy': 'realisedTradeCcy',
        'realised_total': 'realisedTotal',
        'realised_market': 'realisedMarket',
        'realised_currency': 'realisedCurrency'
    }

    required_map = {
        'instrument_scope': 'optional',
        'instrument_uid': 'required',
        'units': 'required',
        'purchase_trade_date': 'optional',
        'purchase_settlement_date': 'optional',
        'purchase_price': 'optional',
        'cost_trade_ccy': 'required',
        'cost_portfolio_ccy': 'required',
        'realised_trade_ccy': 'required',
        'realised_total': 'required',
        'realised_market': 'optional',
        'realised_currency': 'optional'
    }

    def __init__(self, instrument_scope=None, instrument_uid=None, units=None, purchase_trade_date=None, purchase_settlement_date=None, purchase_price=None, cost_trade_ccy=None, cost_portfolio_ccy=None, realised_trade_ccy=None, realised_total=None, realised_market=None, realised_currency=None, local_vars_configuration=None):  # noqa: E501
        """RealisedGainLoss - a model defined in OpenAPI"
        
        :param instrument_scope:  The scope in which the instrument lies.
        :type instrument_scope: str
        :param instrument_uid:  The unqiue Lusid Instrument Id (LUID) of the instrument that this gain or loss is associated with. (required)
        :type instrument_uid: str
        :param units:  The number of units of the associated instrument against which the gain or loss has been realised. (required)
        :type units: float
        :param purchase_trade_date:  The effective datetime that the units associated with this gain or loss where originally purchased.
        :type purchase_trade_date: datetime
        :param purchase_settlement_date:  The effective datetime that the units associated with this gain or loss where originally settled.
        :type purchase_settlement_date: datetime
        :param purchase_price:  The purchase price of each unit associated with this gain or loss.
        :type purchase_price: float
        :param cost_trade_ccy:  (required)
        :type cost_trade_ccy: lusid.CurrencyAndAmount
        :param cost_portfolio_ccy:  (required)
        :type cost_portfolio_ccy: lusid.CurrencyAndAmount
        :param realised_trade_ccy:  (required)
        :type realised_trade_ccy: lusid.CurrencyAndAmount
        :param realised_total:  (required)
        :type realised_total: lusid.CurrencyAndAmount
        :param realised_market: 
        :type realised_market: lusid.CurrencyAndAmount
        :param realised_currency: 
        :type realised_currency: lusid.CurrencyAndAmount

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._instrument_scope = None
        self._instrument_uid = None
        self._units = None
        self._purchase_trade_date = None
        self._purchase_settlement_date = None
        self._purchase_price = None
        self._cost_trade_ccy = None
        self._cost_portfolio_ccy = None
        self._realised_trade_ccy = None
        self._realised_total = None
        self._realised_market = None
        self._realised_currency = None
        self.discriminator = None

        self.instrument_scope = instrument_scope
        self.instrument_uid = instrument_uid
        self.units = units
        self.purchase_trade_date = purchase_trade_date
        self.purchase_settlement_date = purchase_settlement_date
        self.purchase_price = purchase_price
        self.cost_trade_ccy = cost_trade_ccy
        self.cost_portfolio_ccy = cost_portfolio_ccy
        self.realised_trade_ccy = realised_trade_ccy
        self.realised_total = realised_total
        if realised_market is not None:
            self.realised_market = realised_market
        if realised_currency is not None:
            self.realised_currency = realised_currency

    @property
    def instrument_scope(self):
        """Gets the instrument_scope of this RealisedGainLoss.  # noqa: E501

        The scope in which the instrument lies.  # noqa: E501

        :return: The instrument_scope of this RealisedGainLoss.  # noqa: E501
        :rtype: str
        """
        return self._instrument_scope

    @instrument_scope.setter
    def instrument_scope(self, instrument_scope):
        """Sets the instrument_scope of this RealisedGainLoss.

        The scope in which the instrument lies.  # noqa: E501

        :param instrument_scope: The instrument_scope of this RealisedGainLoss.  # noqa: E501
        :type instrument_scope: str
        """

        self._instrument_scope = instrument_scope

    @property
    def instrument_uid(self):
        """Gets the instrument_uid of this RealisedGainLoss.  # noqa: E501

        The unqiue Lusid Instrument Id (LUID) of the instrument that this gain or loss is associated with.  # noqa: E501

        :return: The instrument_uid of this RealisedGainLoss.  # noqa: E501
        :rtype: str
        """
        return self._instrument_uid

    @instrument_uid.setter
    def instrument_uid(self, instrument_uid):
        """Sets the instrument_uid of this RealisedGainLoss.

        The unqiue Lusid Instrument Id (LUID) of the instrument that this gain or loss is associated with.  # noqa: E501

        :param instrument_uid: The instrument_uid of this RealisedGainLoss.  # noqa: E501
        :type instrument_uid: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_uid is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_uid`, must not be `None`")  # noqa: E501

        self._instrument_uid = instrument_uid

    @property
    def units(self):
        """Gets the units of this RealisedGainLoss.  # noqa: E501

        The number of units of the associated instrument against which the gain or loss has been realised.  # noqa: E501

        :return: The units of this RealisedGainLoss.  # noqa: E501
        :rtype: float
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this RealisedGainLoss.

        The number of units of the associated instrument against which the gain or loss has been realised.  # noqa: E501

        :param units: The units of this RealisedGainLoss.  # noqa: E501
        :type units: float
        """
        if self.local_vars_configuration.client_side_validation and units is None:  # noqa: E501
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def purchase_trade_date(self):
        """Gets the purchase_trade_date of this RealisedGainLoss.  # noqa: E501

        The effective datetime that the units associated with this gain or loss where originally purchased.  # noqa: E501

        :return: The purchase_trade_date of this RealisedGainLoss.  # noqa: E501
        :rtype: datetime
        """
        return self._purchase_trade_date

    @purchase_trade_date.setter
    def purchase_trade_date(self, purchase_trade_date):
        """Sets the purchase_trade_date of this RealisedGainLoss.

        The effective datetime that the units associated with this gain or loss where originally purchased.  # noqa: E501

        :param purchase_trade_date: The purchase_trade_date of this RealisedGainLoss.  # noqa: E501
        :type purchase_trade_date: datetime
        """

        self._purchase_trade_date = purchase_trade_date

    @property
    def purchase_settlement_date(self):
        """Gets the purchase_settlement_date of this RealisedGainLoss.  # noqa: E501

        The effective datetime that the units associated with this gain or loss where originally settled.  # noqa: E501

        :return: The purchase_settlement_date of this RealisedGainLoss.  # noqa: E501
        :rtype: datetime
        """
        return self._purchase_settlement_date

    @purchase_settlement_date.setter
    def purchase_settlement_date(self, purchase_settlement_date):
        """Sets the purchase_settlement_date of this RealisedGainLoss.

        The effective datetime that the units associated with this gain or loss where originally settled.  # noqa: E501

        :param purchase_settlement_date: The purchase_settlement_date of this RealisedGainLoss.  # noqa: E501
        :type purchase_settlement_date: datetime
        """

        self._purchase_settlement_date = purchase_settlement_date

    @property
    def purchase_price(self):
        """Gets the purchase_price of this RealisedGainLoss.  # noqa: E501

        The purchase price of each unit associated with this gain or loss.  # noqa: E501

        :return: The purchase_price of this RealisedGainLoss.  # noqa: E501
        :rtype: float
        """
        return self._purchase_price

    @purchase_price.setter
    def purchase_price(self, purchase_price):
        """Sets the purchase_price of this RealisedGainLoss.

        The purchase price of each unit associated with this gain or loss.  # noqa: E501

        :param purchase_price: The purchase_price of this RealisedGainLoss.  # noqa: E501
        :type purchase_price: float
        """

        self._purchase_price = purchase_price

    @property
    def cost_trade_ccy(self):
        """Gets the cost_trade_ccy of this RealisedGainLoss.  # noqa: E501


        :return: The cost_trade_ccy of this RealisedGainLoss.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._cost_trade_ccy

    @cost_trade_ccy.setter
    def cost_trade_ccy(self, cost_trade_ccy):
        """Sets the cost_trade_ccy of this RealisedGainLoss.


        :param cost_trade_ccy: The cost_trade_ccy of this RealisedGainLoss.  # noqa: E501
        :type cost_trade_ccy: lusid.CurrencyAndAmount
        """
        if self.local_vars_configuration.client_side_validation and cost_trade_ccy is None:  # noqa: E501
            raise ValueError("Invalid value for `cost_trade_ccy`, must not be `None`")  # noqa: E501

        self._cost_trade_ccy = cost_trade_ccy

    @property
    def cost_portfolio_ccy(self):
        """Gets the cost_portfolio_ccy of this RealisedGainLoss.  # noqa: E501


        :return: The cost_portfolio_ccy of this RealisedGainLoss.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._cost_portfolio_ccy

    @cost_portfolio_ccy.setter
    def cost_portfolio_ccy(self, cost_portfolio_ccy):
        """Sets the cost_portfolio_ccy of this RealisedGainLoss.


        :param cost_portfolio_ccy: The cost_portfolio_ccy of this RealisedGainLoss.  # noqa: E501
        :type cost_portfolio_ccy: lusid.CurrencyAndAmount
        """
        if self.local_vars_configuration.client_side_validation and cost_portfolio_ccy is None:  # noqa: E501
            raise ValueError("Invalid value for `cost_portfolio_ccy`, must not be `None`")  # noqa: E501

        self._cost_portfolio_ccy = cost_portfolio_ccy

    @property
    def realised_trade_ccy(self):
        """Gets the realised_trade_ccy of this RealisedGainLoss.  # noqa: E501


        :return: The realised_trade_ccy of this RealisedGainLoss.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._realised_trade_ccy

    @realised_trade_ccy.setter
    def realised_trade_ccy(self, realised_trade_ccy):
        """Sets the realised_trade_ccy of this RealisedGainLoss.


        :param realised_trade_ccy: The realised_trade_ccy of this RealisedGainLoss.  # noqa: E501
        :type realised_trade_ccy: lusid.CurrencyAndAmount
        """
        if self.local_vars_configuration.client_side_validation and realised_trade_ccy is None:  # noqa: E501
            raise ValueError("Invalid value for `realised_trade_ccy`, must not be `None`")  # noqa: E501

        self._realised_trade_ccy = realised_trade_ccy

    @property
    def realised_total(self):
        """Gets the realised_total of this RealisedGainLoss.  # noqa: E501


        :return: The realised_total of this RealisedGainLoss.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._realised_total

    @realised_total.setter
    def realised_total(self, realised_total):
        """Sets the realised_total of this RealisedGainLoss.


        :param realised_total: The realised_total of this RealisedGainLoss.  # noqa: E501
        :type realised_total: lusid.CurrencyAndAmount
        """
        if self.local_vars_configuration.client_side_validation and realised_total is None:  # noqa: E501
            raise ValueError("Invalid value for `realised_total`, must not be `None`")  # noqa: E501

        self._realised_total = realised_total

    @property
    def realised_market(self):
        """Gets the realised_market of this RealisedGainLoss.  # noqa: E501


        :return: The realised_market of this RealisedGainLoss.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._realised_market

    @realised_market.setter
    def realised_market(self, realised_market):
        """Sets the realised_market of this RealisedGainLoss.


        :param realised_market: The realised_market of this RealisedGainLoss.  # noqa: E501
        :type realised_market: lusid.CurrencyAndAmount
        """

        self._realised_market = realised_market

    @property
    def realised_currency(self):
        """Gets the realised_currency of this RealisedGainLoss.  # noqa: E501


        :return: The realised_currency of this RealisedGainLoss.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._realised_currency

    @realised_currency.setter
    def realised_currency(self, realised_currency):
        """Sets the realised_currency of this RealisedGainLoss.


        :param realised_currency: The realised_currency of this RealisedGainLoss.  # noqa: E501
        :type realised_currency: lusid.CurrencyAndAmount
        """

        self._realised_currency = realised_currency

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
        if not isinstance(other, RealisedGainLoss):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RealisedGainLoss):
            return True

        return self.to_dict() != other.to_dict()
