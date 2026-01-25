[**rmapi-js**](../README.md)

***

# Interface: Entries

Defined in: [raw.ts:79](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L79)

a parsed entries file

id and size are defined for schema 4 but not for 3

## Properties

<a id="entries"></a>

### entries

> **entries**: [`RawEntry`](RawEntry.md)[]

Defined in: [raw.ts:81](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L81)

the raw entries in the file

***

<a id="id"></a>

### id?

> `optional` **id**: `string`

Defined in: [raw.ts:83](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L83)

the id of this entry, only specified for schema 4

***

<a id="size"></a>

### size?

> `optional` **size**: `number`

Defined in: [raw.ts:85](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L85)

the recursive size of this entry, only specified for schema 4
