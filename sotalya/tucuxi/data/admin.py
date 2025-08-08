#!/usr/bin/python3
from dataclasses import dataclass


@dataclass
class Institute:
    instituteId: str
    name: str
    street: str
    postalCode: str
    city: str
    state: str
    country: str
    phoneNumber: str
    phoneType: str
    emailAddress: str
    emailType: str

    @staticmethod
    def create_from_soup(soup):
        instituteId = soup.instituteId.string
        name = soup.name.string
        street = soup.street.string
        postalCode = soup.postalCode.string
        city = soup.city.string
        state = soup.state.string
        country = soup.country.string
        phoneNumber = soup.phoneNumber.string
        phoneType = soup.phoneType.string
        emailAddress = soup.emailAddress.string
        emailType = soup.emailType.string

        return Institute(
            instituteId, name,
            street, postalCode, city, state, country,
            phoneNumber, phoneType,
            emailAddress, emailType,
        )


@dataclass
class Person:
    personId: str
    title: str
    firstName: str
    lastName: str
    street: str
    postalCode: str
    city: str
    state: str
    country: str
    phoneNumber: str
    phoneType: str
    emailAddress: str
    emailType: str

    @staticmethod
    def create_from_soup(soup):
        personId = soup.personId.string
        title = soup.title.string
        firstName = soup.firstName.string
        lastName = soup.lastName.string
        street = soup.street.string
        postalCode = soup.postalCode.string
        city = soup.city.string
        state = soup.state.string
        country = soup.country.string
        phoneNumber = soup.phoneNumber.string
        phoneType = soup.phoneType.string
        emailAddress = soup.emailAddress.string
        emailType = soup.emailType.string

        return Person(
            personId, firstName, lastName,
            street, postalCode, city, state, country,
            phoneNumber, phoneType,
            emailAddress, emailType,
        )
