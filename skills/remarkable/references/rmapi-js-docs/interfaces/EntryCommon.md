[**rmapi-js**](../README.md)

***

# Interface: EntryCommon

Defined in: [index.ts:121](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L121)

common properties shared by collections and documents

## Extended by

- [`CollectionEntry`](CollectionEntry.md)
- [`DocumentType`](DocumentType.md)
- [`TemplateType`](TemplateType.md)

## Properties

<a id="hash"></a>

### hash

> **hash**: `string`

Defined in: [index.ts:125](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L125)

the current hash of the state of this entry

***

<a id="id"></a>

### id

> **id**: `string`

Defined in: [index.ts:123](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L123)

the document id, a uuid4

***

<a id="lastmodified"></a>

### lastModified

> **lastModified**: `string`

Defined in: [index.ts:129](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L129)

the last modified timestamp

***

<a id="pinned"></a>

### pinned

> **pinned**: `boolean`

Defined in: [index.ts:131](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L131)

true if the entry is starred in most ui elements

***

<a id="visiblename"></a>

### visibleName

> **visibleName**: `string`

Defined in: [index.ts:127](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L127)

the visible display name of this entry

***

<a id="parent"></a>

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:138](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L138)

the parent of this entry

There are two special parents, "" (empty string) for the root directory,
and "trash" for the trash

***

<a id="tags"></a>

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [index.ts:140](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L140)

any tags the entry might have
