[**rmapi-js**](../README.md)

***

# Class: ValidationError

Defined in: [error.ts:2](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L2)

an error that results from a failed request

## Extends

- `Error`

## Constructors

<a id="constructor"></a>

### Constructor

> **new ValidationError**(`field`, `regex`, `message`): `ValidationError`

Defined in: [error.ts:8](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L8)

#### Parameters

##### field

`string`

##### regex

`RegExp`

##### message

`string`

#### Returns

`ValidationError`

#### Overrides

`Error.constructor`

## Properties

<a id="field"></a>

### field

> `readonly` **field**: `string`

Defined in: [error.ts:4](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L4)

the response status number

***

<a id="regex"></a>

### regex

> `readonly` **regex**: `RegExp`

Defined in: [error.ts:6](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L6)

the response status text
