[**rmapi-js**](../README.md)

***

# Class: HashNotFoundError

Defined in: [error.ts:16](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L16)

an error that results while supplying a hash not found in the entries of the root hash

## Extends

- `Error`

## Constructors

<a id="constructor"></a>

### Constructor

> **new HashNotFoundError**(`hash`): `HashNotFoundError`

Defined in: [error.ts:20](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L20)

#### Parameters

##### hash

`string`

#### Returns

`HashNotFoundError`

#### Overrides

`Error.constructor`

## Properties

<a id="hash"></a>

### hash

> `readonly` **hash**: `string`

Defined in: [error.ts:18](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/error.ts#L18)

the hash that couldn't be found
