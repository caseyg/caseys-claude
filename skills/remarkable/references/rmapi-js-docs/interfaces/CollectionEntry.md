[**rmapi-js**](../README.md)

***

# Interface: CollectionEntry

Defined in: [index.ts:144](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L144)

a folder, referred to in the api as a collection

## Extends

- [`EntryCommon`](EntryCommon.md)

## Properties

<a id="hash"></a>

### hash

> **hash**: `string`

Defined in: [index.ts:125](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L125)

the current hash of the state of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`hash`](EntryCommon.md#hash)

***

<a id="id"></a>

### id

> **id**: `string`

Defined in: [index.ts:123](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L123)

the document id, a uuid4

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`id`](EntryCommon.md#id)

***

<a id="lastmodified"></a>

### lastModified

> **lastModified**: `string`

Defined in: [index.ts:129](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L129)

the last modified timestamp

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`lastModified`](EntryCommon.md#lastmodified)

***

<a id="pinned"></a>

### pinned

> **pinned**: `boolean`

Defined in: [index.ts:131](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L131)

true if the entry is starred in most ui elements

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`pinned`](EntryCommon.md#pinned)

***

<a id="type"></a>

### type

> **type**: `"CollectionType"`

Defined in: [index.ts:146](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L146)

the key for this as a collection

***

<a id="visiblename"></a>

### visibleName

> **visibleName**: `string`

Defined in: [index.ts:127](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L127)

the visible display name of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`visibleName`](EntryCommon.md#visiblename)

***

<a id="parent"></a>

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:138](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L138)

the parent of this entry

There are two special parents, "" (empty string) for the root directory,
and "trash" for the trash

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`parent`](EntryCommon.md#parent)

***

<a id="tags"></a>

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [index.ts:140](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L140)

any tags the entry might have

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`tags`](EntryCommon.md#tags)
