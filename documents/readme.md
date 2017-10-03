## readme 

Don't edit the markdown files

You can sortof track the changes here by installing 
[pandoc](http://pandoc.org/installing.html), and adding the folowing to 
your `~/.gitconfig` file:

```
# .gitconfig file in your home folder
[diff "pandoc"]
  textconv=pandoc --to=markdown
  prompt = false
[alias]
  wdiff = diff --word-diff=color --unified=1
```

Adapted from [Using Microsoft Word with 
git](http://blog.martinfenner.org/2014/08/25/using-microsoft-word-with-git/), 
and [Integrate git diffs with word docx 
files](https://github.com/vigente/gerardus/wiki/Integrate-git-diffs-with-word-docx-files)
