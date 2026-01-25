[**rmapi-js**](../README.md)

***

# Function: session()

> **session**(`sessionToken`, `__namedParameters`): [`RemarkableApi`](../interfaces/RemarkableApi.md)

Defined in: [index.ts:1552](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1552)

Create an API instance from an existing session token.

If requests start failing, simply recreate the api instance with a freshly
fetched session token.

## Parameters

### sessionToken

`string`

the session token used for authorization

### \_\_namedParameters

[`RemarkableSessionOptions`](../interfaces/RemarkableSessionOptions.md) = `{}`

## Returns

[`RemarkableApi`](../interfaces/RemarkableApi.md)

an api instance
