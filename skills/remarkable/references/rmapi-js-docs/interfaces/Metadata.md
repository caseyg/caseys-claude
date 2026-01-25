[**rmapi-js**](../README.md)

***

# Interface: Metadata

Defined in: [raw.ts:578](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L578)

item level metadata

Stored with the extension "metadata".

## Properties

<a id="lastmodified"></a>

### lastModified

> **lastModified**: `string`

Defined in: [raw.ts:584](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L584)

the last modify time, the string of the epoch timestamp

***

<a id="parent"></a>

### parent

> **parent**: `string`

Defined in: [raw.ts:599](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L599)

the id of the parent collection

This is the empty string for root (no parent), "trash" if it's in the
trash, or the id of the parent.

***

<a id="pinned"></a>

### pinned

> **pinned**: `boolean`

Defined in: [raw.ts:601](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L601)

true of the item is starred

***

<a id="type"></a>

### type

> **type**: `"DocumentType"` \| `"CollectionType"` \| `"TemplateType"`

Defined in: [raw.ts:610](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L610)

the type of item this corresponds to

DocumentType is a document, an epub, pdf, or notebook, CollectionType is a
folder.

***

<a id="visiblename"></a>

### visibleName

> **visibleName**: `string`

Defined in: [raw.ts:622](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L622)

the visible name of the item, what it's called on the reMarkable

***

<a id="createdtime"></a>

### createdTime?

> `optional` **createdTime**: `string`

Defined in: [raw.ts:580](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L580)

creation time, a string of the epoch timestamp

***

<a id="deleted"></a>

### deleted?

> `optional` **deleted**: `boolean`

Defined in: [raw.ts:582](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L582)

[speculative] true if the item has been actually deleted

***

<a id="lastopened"></a>

### lastOpened?

> `optional` **lastOpened**: `string`

Defined in: [raw.ts:586](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L586)

the last opened epoch timestamp, isn't defined for CollectionType

***

<a id="lastopenedpage"></a>

### lastOpenedPage?

> `optional` **lastOpenedPage**: `number`

Defined in: [raw.ts:588](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L588)

the last page opened, isn't defined for CollectionType, starts at 0

***

<a id="metadatamodified"></a>

### metadatamodified?

> `optional` **metadatamodified**: `boolean`

Defined in: [raw.ts:590](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L590)

[speculative] true if the metadata has been modified

***

<a id="modified"></a>

### modified?

> `optional` **modified**: `boolean`

Defined in: [raw.ts:592](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L592)

[speculative] true if the item has been modified

***

<a id="new"></a>

### new?

> `optional` **new**: `boolean`

Defined in: [raw.ts:612](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L612)

whether this is this a newly-installed template

***

<a id="source"></a>

### source?

> `optional` **source**: `string`

Defined in: [raw.ts:618](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L618)

the provider from which this item was obtained/installed

Example: a template from "com.remarkable.methods".

***

<a id="synced"></a>

### synced?

> `optional` **synced**: `boolean`

Defined in: [raw.ts:603](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L603)

[unknown]

***

<a id="version"></a>

### version?

> `optional` **version**: `number`

Defined in: [raw.ts:620](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L620)

[speculative] metadata version, always 0
