[**rmapi-js**](../README.md)

***

# Class: GenerationError

Defined in: [index.ts:201](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L201)

An error that gets thrown when the backend while trying to update

IF you encounter this error, you likely just need to try th request again. If
you're trying to do several high-level `put` operations simultaneously,
you'll likely encounter this error. You should either try to do them
serially, or call the low level api directly to do one generation update.

## See

[\`RawRemarkableApi\`](../interfaces/RawRemarkableApi.md)

## Extends

- `Error`

## Constructors

<a id="constructor"></a>

### Constructor

> **new GenerationError**(): `GenerationError`

Defined in: [index.ts:202](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L202)

#### Returns

`GenerationError`

#### Overrides

`Error.constructor`
