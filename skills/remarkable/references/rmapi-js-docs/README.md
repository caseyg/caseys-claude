**rmapi-js**

***

# rmapi-js

Create and interact with reMarkable cloud.

After getting a device token with the [\`register\`](functions/register.md) method,
persist it and create api instances using [\`remarkable\`](functions/remarkable.md).
Outside of registration, all relevant methods are in
[\`RemarkableApi\`](interfaces/RemarkableApi.md), or it's interior
[\`RawRemarkableApi\`](interfaces/RawRemarkableApi.md) (for lower level functions).

## Examples

A simple rename
```ts
import { register, remarkable } from "rmapi-js";

const code = "..."  // eight letter code from https://my.remarkable.com/device/browser/connect
const token = await register(code)
// persist token
const api = await remarkable(token);
// list all items (documents and collections)
const [first, ...rest] = api.listItems();
// rename first item
const entry = api.rename(first.hash, "new name");
```

A simple upload
```ts
import { remarkable } from "rmapi-js";

const api = await remarkable(...);
const entry = await api.putEpub("document name", epubBuffer);
```

## Remarks

The cloud api is essentially a collection of entries. Each entry has an id,
which is a uuid4 and a hash, which indicates it's current state, and changes
as the item mutates, where the id is constant. Most mutable operations take
the initial hash so that merge conflicts can be resolved. Each entry has a
number of properties, but a key property is the `parent`, which represents
its parent in the file structure. This will be another document id, or one of
two special ids, "" (the empty string) for the root directory, or "trash" for
the trash.

Detailed information about the low-level storage an apis can be found in
[\`RawRemarkableApi\`](interfaces/RawRemarkableApi.md).

Additionally, this entire api was reverse engineered, so some things are only
`[speculative]`, or entirely `[unknown]`. If something breaks, please
[file an issue!](https://github.com/erikbrinkman/rmapi-js/issues)

## Classes

- [GenerationError](classes/GenerationError.md)
- [HashNotFoundError](classes/HashNotFoundError.md)
- [ResponseError](classes/ResponseError.md)
- [ValidationError](classes/ValidationError.md)

## Interfaces

- [AuthOptions](interfaces/AuthOptions.md)
- [CollectionContent](interfaces/CollectionContent.md)
- [CollectionEntry](interfaces/CollectionEntry.md)
- [CPageNumberValue](interfaces/CPageNumberValue.md)
- [CPagePage](interfaces/CPagePage.md)
- [CPages](interfaces/CPages.md)
- [CPageStringValue](interfaces/CPageStringValue.md)
- [CPageUUID](interfaces/CPageUUID.md)
- [DocumentContent](interfaces/DocumentContent.md)
- [DocumentMetadata](interfaces/DocumentMetadata.md)
- [DocumentType](interfaces/DocumentType.md)
- [Entries](interfaces/Entries.md)
- [EntryCommon](interfaces/EntryCommon.md)
- [FolderOptions](interfaces/FolderOptions.md)
- [HashEntry](interfaces/HashEntry.md)
- [HashesEntry](interfaces/HashesEntry.md)
- [KeyboardMetadata](interfaces/KeyboardMetadata.md)
- [Metadata](interfaces/Metadata.md)
- [PageTag](interfaces/PageTag.md)
- [PutOptions](interfaces/PutOptions.md)
- [RawEntry](interfaces/RawEntry.md)
- [RawRemarkableApi](interfaces/RawRemarkableApi.md)
- [RegisterOptions](interfaces/RegisterOptions.md)
- [RemarkableApi](interfaces/RemarkableApi.md)
- [RemarkableOptions](interfaces/RemarkableOptions.md)
- [RemarkableSessionOptions](interfaces/RemarkableSessionOptions.md)
- [SimpleEntry](interfaces/SimpleEntry.md)
- [Tag](interfaces/Tag.md)
- [TemplateContent](interfaces/TemplateContent.md)
- [TemplateType](interfaces/TemplateType.md)

## Type Aliases

- [BackgroundFilter](type-aliases/BackgroundFilter.md)
- [Content](type-aliases/Content.md)
- [Entry](type-aliases/Entry.md)
- [FileType](type-aliases/FileType.md)
- [Orientation](type-aliases/Orientation.md)
- [SchemaVersion](type-aliases/SchemaVersion.md)
- [TextAlignment](type-aliases/TextAlignment.md)
- [UploadMimeType](type-aliases/UploadMimeType.md)
- [ZoomMode](type-aliases/ZoomMode.md)

## Functions

- [auth](functions/auth.md)
- [register](functions/register.md)
- [remarkable](functions/remarkable.md)
- [session](functions/session.md)
