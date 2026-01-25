[**rmapi-js**](../README.md)

***

# Interface: RemarkableOptions

Defined in: [index.ts:1511](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1511)

options for a remarkable instance

## Extends

- [`AuthOptions`](AuthOptions.md).[`RemarkableSessionOptions`](RemarkableSessionOptions.md)

## Properties

<a id="authhost"></a>

### authHost?

> `optional` **authHost**: `string`

Defined in: [index.ts:1464](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1464)

the url for making authorization requests

#### Default Value

```ts
"https://webapp-prod.cloud.remarkable.engineering"
```

#### Inherited from

[`AuthOptions`](AuthOptions.md).[`authHost`](AuthOptions.md#authhost)

***

<a id="cache"></a>

### cache?

> `optional` **cache**: `string`

Defined in: [index.ts:1496](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1496)

an initial cache value

Generated from calling [\`dumpCache\`](RemarkableApi.md#dumpcache) on a previous
instance.

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`cache`](RemarkableSessionOptions.md#cache)

***

<a id="maxcachesize"></a>

### maxCacheSize?

> `optional` **maxCacheSize**: `number`

Defined in: [index.ts:1507](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1507)

the maximum size of the cache in terms of total string length

By the JavaScript specification there are two bytes per character, but the
total memory usage of the cache will also be larger than just the size of
the data stored.

#### Default Value

```ts
Infinity
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`maxCacheSize`](RemarkableSessionOptions.md#maxcachesize)

***

<a id="rawhost"></a>

### rawHost?

> `optional` **rawHost**: `string`

Defined in: [index.ts:1488](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1488)

the url for making requests using the low-level api

#### Default Value

```ts
"https://eu.tectonic.remarkable.com"
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`rawHost`](RemarkableSessionOptions.md#rawhost)

***

<a id="synchost"></a>

### syncHost?

> `optional` **syncHost**: `string`

Defined in: [index.ts:1474](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1474)

the url for making synchronization requests

#### Default Value

```ts
"https://web.eu.tectonic.remarkable.com"
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`syncHost`](RemarkableSessionOptions.md#synchost)

***

<a id="uploadhost"></a>

### uploadHost?

> `optional` **uploadHost**: `string`

Defined in: [index.ts:1481](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1481)

the base url for making upload requests

#### Default Value

```ts
"https://internal.cloud.remarkable.com"
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`uploadHost`](RemarkableSessionOptions.md#uploadhost)
