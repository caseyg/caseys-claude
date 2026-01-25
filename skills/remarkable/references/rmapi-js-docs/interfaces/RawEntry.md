[**rmapi-js**](../README.md)

***

# Interface: RawEntry

Defined in: [raw.ts:58](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L58)

the low-level entry corresponding to a collection of files

A collection could be for the root collection, or for an individual document,
which is often a collection of files. If an entry represents a collection of
files, the high level entry will have the same hash and id as the low-level
entry for that collection.

## Properties

<a id="hash"></a>

### hash

> **hash**: `string`

Defined in: [raw.ts:62](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L62)

the hash of the collection this points to

***

<a id="id"></a>

### id

> **id**: `string`

Defined in: [raw.ts:64](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L64)

the unique id of the collection

***

<a id="size"></a>

### size

> **size**: `number`

Defined in: [raw.ts:68](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L68)

the total size of everything in the collection

***

<a id="subfiles"></a>

### subfiles

> **subfiles**: `number`

Defined in: [raw.ts:66](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L66)

the number of subfiles

***

<a id="type"></a>

### type

> **type**: `0` \| `80000000`

Defined in: [raw.ts:60](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L60)

80000000 for schema 3 collection type or 0 for schema 4 or schema 3 files or
