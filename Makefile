env:
        python -m venv .env

package:
        pip wheel -w dist/ .

upload:
        twine upload dist/chia_plot_manager*.whl
