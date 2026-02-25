# Building an object from many files (SVG example)

If you have many files in one folder and want to reference them by key in code, create a map object where each key points to the file URL.

## Option 1 (recommended for front-end bundlers like Vite)

Use `import.meta.glob` to auto-import all SVG files and turn them into an object.

```js
// src/icons.js
const files = import.meta.glob('./assets/icons/*.svg', {
  eager: true,
  import: 'default',
});

export const icons = Object.fromEntries(
  Object.entries(files).map(([path, url]) => {
    const fileName = path.split('/').pop().replace('.svg', '');
    return [fileName, url];
  })
);
```

Usage:

```js
import { icons } from './icons';

const img = document.createElement('img');
img.src = icons['home']; // src/assets/icons/home.svg
img.alt = 'home';
document.body.appendChild(img);
```

## Option 2 (Node script that generates a map file)

If your stack does not support `import.meta.glob`, generate an object file from the folder.

```js
// scripts/generate-icons-map.mjs
import fs from 'node:fs';
import path from 'node:path';

const dir = 'public/icons';
const outFile = 'src/icons.generated.js';

const svgFiles = fs.readdirSync(dir).filter((f) => f.endsWith('.svg'));

const mapEntries = svgFiles
  .map((f) => {
    const key = path.basename(f, '.svg');
    return `  "${key}": "/icons/${f}"`;
  })
  .join(',\n');

const output = `export const icons = {\n${mapEntries}\n};\n`;
fs.writeFileSync(outFile, output);
console.log(`Generated ${outFile} with ${svgFiles.length} icons.`);
```

Then import `icons.generated.js` and use `icons[key]` as your `<img src>`.
