[**rmapi-js**](../README.md)

***

# Class: ResponseError

Defined in: [index.ts:208](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L208)

an error that results from a failed request

## Extends

- `Error`

## Constructors

<a id="constructor"></a>

### Constructor

> **new ResponseError**(`status`, `statusText`, `message`): `ResponseError`

Defined in: [index.ts:214](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L214)

#### Parameters

##### status

`number`

##### statusText

`string`

##### message

`string`

#### Returns

`ResponseError`

#### Overrides

`Error.constructor`

## Properties

<a id="status"></a>

### status

> `readonly` **status**: `number`

Defined in: [index.ts:210](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L210)

the response status number

***

<a id="statustext"></a>

### statusText

> `readonly` **statusText**: `string`

Defined in: [index.ts:212](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L212)

the response status text
