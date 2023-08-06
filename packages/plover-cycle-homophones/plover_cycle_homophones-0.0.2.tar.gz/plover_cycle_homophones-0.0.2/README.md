# Plover Cycle through homophones 

Companion plugin for BépoSténo - includes the following macros:
- **split_previous**
  split the last word's two last syllables. This is in case plover reads the last two strokes as a single word (eg "A-LAn" turning into "allant" when you want "a lent")
- **find_homophone**
  cycles through homophones from the dictionnary

## Usage
- **Cycle through homophones**:

  add a stroke to your Plover dictionnary in the following format: `"<stroke>": "=find_homophone",`

- For **split_previous**:

  This functionality is tricky. The expected behaviour here, is that for any stroke that calls the macro while containing the splitter key, it will split the previous word's last stroke and attach it to the current one. 

  Here's an example:

  ![Demo usage](https://github.com/AntoineBalaine/plover_cycle_homophones/blob/main/demo_assets/Peek%202022-11-21%2015-32.gif)

  In the first line, we see the second stroke attaches erroneously to the first stroke.
  In the second line, the same thing happens, but the macros gets called, splits the second stroke and attaches it to the third one.

  In order to achieve this functionality, there is sadly no way other than associating every stroke available in your dictionnary to your a splitter key. This means creating a copy of every single stroke of the dictionnary, adding the splitter key inside of it, and binding them to a call of the macro. The splitter key must be at the end of the steno order, optionnally a suffix stroke.
  In the following example, I associated the `ß` symbol to the splitter key. It follows the traditionnal format `"<stroke><splitter_key>": "=split_previous"`

```
{
"SKPREDCß": "=split_previous",
"SKPIlß": "=split_previous",
"SKPInCß": "=split_previous",
"SKPIß": "=split_previous",
"SKMECß": "=split_previous",
}
```
  Currently, the key is hardcoded on line 30 in `split_previous/__init__.py` to `ß`, so you'll have to change that to whatever suits your needs.

  In these conditions, **how do I create a copy of every single stroke in the dictionnary?**. A good starting point would be to use the following command in your dictionnary's directory: 

```
jq 'keys' * | sed -e 's/\//",\n"/g' -e 's/^\s*//' | sort --unique | awk '!/[\[|\]]/' | sed -e '/[\\.]/d' -e '/,"/d' -e 's/"$/",/' -e 's/",/ß":"=space_or_split",/' -e 's/,$//' -e '1s/^/{\n/' -e 's/$/,/' | sort --unique | sed -e '$s/,$/\n}/' 
```
