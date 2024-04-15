#sphinx-build: the following arguments are required: sourcedir, outputdir, filenames
SPHINXBUILD=sphinx-build
SOURCEDIR=doc
BUILDDIR=docs

# change to project directory. -- return to current dir after execution of this script.
while true ; do
	if [[ $PWD == "/" ]]; then
		echo "we could not find the project directory gerber_writer"
		exit 
	fi
#    echo "base=$(basename $PWD) on path $PWD"
    if [[ "$(basename $PWD)" =~ "gerber_writer" ]]; then
      echo "pwd = $PWD"
        break
    fi
    cd ..
done

cp README.rst doc
if [ -z "$1" ]
then
  echo "\nargument missing." 
  $SPHINXBUILD -M help $SOURCEDIR $BUILDDIR
else
  $SPHINXBUILD -M $1 $SOURCEDIR $BUILDDIR
#   $SPHINXOPTS $O
fi

touch docs/.nojekyll
touch docs/html/.nojekyll
