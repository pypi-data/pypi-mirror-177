# coding: utf-8

"""
    DocRaptor

    A native client library for the DocRaptor HTML to PDF/XLS service.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from docraptor.configuration import Configuration


class DocStatus(object):
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
    """
    openapi_types = {
        'status': 'str',
        'download_url': 'str',
        'download_id': 'str',
        'message': 'str',
        'number_of_pages': 'int',
        'validation_errors': 'str'
    }

    attribute_map = {
        'status': 'status',
        'download_url': 'download_url',
        'download_id': 'download_id',
        'message': 'message',
        'number_of_pages': 'number_of_pages',
        'validation_errors': 'validation_errors'
    }

    def __init__(self, status=None, download_url=None, download_id=None, message=None, number_of_pages=None, validation_errors=None, local_vars_configuration=None):  # noqa: E501
        """DocStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._status = None
        self._download_url = None
        self._download_id = None
        self._message = None
        self._number_of_pages = None
        self._validation_errors = None
        self.discriminator = None

        if status is not None:
            self.status = status
        if download_url is not None:
            self.download_url = download_url
        if download_id is not None:
            self.download_id = download_id
        if message is not None:
            self.message = message
        if number_of_pages is not None:
            self.number_of_pages = number_of_pages
        if validation_errors is not None:
            self.validation_errors = validation_errors

    @property
    def status(self):
        """Gets the status of this DocStatus.  # noqa: E501

        The present status of the document. Can be queued, working, completed, and failed.  # noqa: E501

        :return: The status of this DocStatus.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DocStatus.

        The present status of the document. Can be queued, working, completed, and failed.  # noqa: E501

        :param status: The status of this DocStatus.  # noqa: E501
        :type status: str
        """

        self._status = status

    @property
    def download_url(self):
        """Gets the download_url of this DocStatus.  # noqa: E501

        The URL where the document can be retrieved. This URL may only be used a few times.  # noqa: E501

        :return: The download_url of this DocStatus.  # noqa: E501
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """Sets the download_url of this DocStatus.

        The URL where the document can be retrieved. This URL may only be used a few times.  # noqa: E501

        :param download_url: The download_url of this DocStatus.  # noqa: E501
        :type download_url: str
        """

        self._download_url = download_url

    @property
    def download_id(self):
        """Gets the download_id of this DocStatus.  # noqa: E501

        The identifier for downloading the document with the download API.  # noqa: E501

        :return: The download_id of this DocStatus.  # noqa: E501
        :rtype: str
        """
        return self._download_id

    @download_id.setter
    def download_id(self, download_id):
        """Sets the download_id of this DocStatus.

        The identifier for downloading the document with the download API.  # noqa: E501

        :param download_id: The download_id of this DocStatus.  # noqa: E501
        :type download_id: str
        """

        self._download_id = download_id

    @property
    def message(self):
        """Gets the message of this DocStatus.  # noqa: E501

        Additional information.  # noqa: E501

        :return: The message of this DocStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this DocStatus.

        Additional information.  # noqa: E501

        :param message: The message of this DocStatus.  # noqa: E501
        :type message: str
        """

        self._message = message

    @property
    def number_of_pages(self):
        """Gets the number_of_pages of this DocStatus.  # noqa: E501

        Number of PDF pages in document.  # noqa: E501

        :return: The number_of_pages of this DocStatus.  # noqa: E501
        :rtype: int
        """
        return self._number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, number_of_pages):
        """Sets the number_of_pages of this DocStatus.

        Number of PDF pages in document.  # noqa: E501

        :param number_of_pages: The number_of_pages of this DocStatus.  # noqa: E501
        :type number_of_pages: int
        """

        self._number_of_pages = number_of_pages

    @property
    def validation_errors(self):
        """Gets the validation_errors of this DocStatus.  # noqa: E501

        Error information.  # noqa: E501

        :return: The validation_errors of this DocStatus.  # noqa: E501
        :rtype: str
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """Sets the validation_errors of this DocStatus.

        Error information.  # noqa: E501

        :param validation_errors: The validation_errors of this DocStatus.  # noqa: E501
        :type validation_errors: str
        """

        self._validation_errors = validation_errors

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
        if not isinstance(other, DocStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DocStatus):
            return True

        return self.to_dict() != other.to_dict()
