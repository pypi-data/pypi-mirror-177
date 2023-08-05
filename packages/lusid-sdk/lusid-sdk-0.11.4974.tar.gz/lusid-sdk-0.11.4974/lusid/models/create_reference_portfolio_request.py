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


class CreateReferencePortfolioRequest(object):
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
        'display_name': 'str',
        'description': 'str',
        'code': 'str',
        'created': 'datetime',
        'properties': 'dict(str, ModelProperty)',
        'instrument_scopes': 'list[str]',
        'base_currency': 'str'
    }

    attribute_map = {
        'display_name': 'displayName',
        'description': 'description',
        'code': 'code',
        'created': 'created',
        'properties': 'properties',
        'instrument_scopes': 'instrumentScopes',
        'base_currency': 'baseCurrency'
    }

    required_map = {
        'display_name': 'required',
        'description': 'optional',
        'code': 'required',
        'created': 'optional',
        'properties': 'optional',
        'instrument_scopes': 'optional',
        'base_currency': 'optional'
    }

    def __init__(self, display_name=None, description=None, code=None, created=None, properties=None, instrument_scopes=None, base_currency=None, local_vars_configuration=None):  # noqa: E501
        """CreateReferencePortfolioRequest - a model defined in OpenAPI"
        
        :param display_name:  The name of the reference portfolio. (required)
        :type display_name: str
        :param description:  A long form text description of the portfolio.
        :type description: str
        :param code:  Unique identifier for the portfolio. (required)
        :type code: str
        :param created:  The original creation date, defaults to today if not specified when creating a portfolio.
        :type created: datetime
        :param properties:  Portfolio properties to add to the portfolio.
        :type properties: dict[str, lusid.ModelProperty]
        :param instrument_scopes:  Instrument Scopes.
        :type instrument_scopes: list[str]
        :param base_currency:  The base currency of the transaction portfolio in ISO 4217 currency code format.
        :type base_currency: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._display_name = None
        self._description = None
        self._code = None
        self._created = None
        self._properties = None
        self._instrument_scopes = None
        self._base_currency = None
        self.discriminator = None

        self.display_name = display_name
        self.description = description
        self.code = code
        self.created = created
        self.properties = properties
        self.instrument_scopes = instrument_scopes
        self.base_currency = base_currency

    @property
    def display_name(self):
        """Gets the display_name of this CreateReferencePortfolioRequest.  # noqa: E501

        The name of the reference portfolio.  # noqa: E501

        :return: The display_name of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this CreateReferencePortfolioRequest.

        The name of the reference portfolio.  # noqa: E501

        :param display_name: The display_name of this CreateReferencePortfolioRequest.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this CreateReferencePortfolioRequest.  # noqa: E501

        A long form text description of the portfolio.  # noqa: E501

        :return: The description of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateReferencePortfolioRequest.

        A long form text description of the portfolio.  # noqa: E501

        :param description: The description of this CreateReferencePortfolioRequest.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def code(self):
        """Gets the code of this CreateReferencePortfolioRequest.  # noqa: E501

        Unique identifier for the portfolio.  # noqa: E501

        :return: The code of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this CreateReferencePortfolioRequest.

        Unique identifier for the portfolio.  # noqa: E501

        :param code: The code of this CreateReferencePortfolioRequest.  # noqa: E501
        :type code: str
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def created(self):
        """Gets the created of this CreateReferencePortfolioRequest.  # noqa: E501

        The original creation date, defaults to today if not specified when creating a portfolio.  # noqa: E501

        :return: The created of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this CreateReferencePortfolioRequest.

        The original creation date, defaults to today if not specified when creating a portfolio.  # noqa: E501

        :param created: The created of this CreateReferencePortfolioRequest.  # noqa: E501
        :type created: datetime
        """

        self._created = created

    @property
    def properties(self):
        """Gets the properties of this CreateReferencePortfolioRequest.  # noqa: E501

        Portfolio properties to add to the portfolio.  # noqa: E501

        :return: The properties of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: dict[str, lusid.ModelProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this CreateReferencePortfolioRequest.

        Portfolio properties to add to the portfolio.  # noqa: E501

        :param properties: The properties of this CreateReferencePortfolioRequest.  # noqa: E501
        :type properties: dict[str, lusid.ModelProperty]
        """

        self._properties = properties

    @property
    def instrument_scopes(self):
        """Gets the instrument_scopes of this CreateReferencePortfolioRequest.  # noqa: E501

        Instrument Scopes.  # noqa: E501

        :return: The instrument_scopes of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._instrument_scopes

    @instrument_scopes.setter
    def instrument_scopes(self, instrument_scopes):
        """Sets the instrument_scopes of this CreateReferencePortfolioRequest.

        Instrument Scopes.  # noqa: E501

        :param instrument_scopes: The instrument_scopes of this CreateReferencePortfolioRequest.  # noqa: E501
        :type instrument_scopes: list[str]
        """

        self._instrument_scopes = instrument_scopes

    @property
    def base_currency(self):
        """Gets the base_currency of this CreateReferencePortfolioRequest.  # noqa: E501

        The base currency of the transaction portfolio in ISO 4217 currency code format.  # noqa: E501

        :return: The base_currency of this CreateReferencePortfolioRequest.  # noqa: E501
        :rtype: str
        """
        return self._base_currency

    @base_currency.setter
    def base_currency(self, base_currency):
        """Sets the base_currency of this CreateReferencePortfolioRequest.

        The base currency of the transaction portfolio in ISO 4217 currency code format.  # noqa: E501

        :param base_currency: The base_currency of this CreateReferencePortfolioRequest.  # noqa: E501
        :type base_currency: str
        """

        self._base_currency = base_currency

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
        if not isinstance(other, CreateReferencePortfolioRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateReferencePortfolioRequest):
            return True

        return self.to_dict() != other.to_dict()
