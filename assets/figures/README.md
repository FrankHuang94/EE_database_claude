# Figures

Generated figures, committed so that chapters render on GitHub without running anything. Every figure is produced by a script in [src/](src/), one script per chapter (`fig_NN_MM.py`). Scripts use the shared style in [tools/plotstyle.py](../../tools/plotstyle.py): white background, so figures read well in both light and dark themes, and a colorblind-safe palette.

To regenerate all figures:

```bash
make figures
```

Output folders are named after the chapter (`assets/figures/NN-MM/`). SVG is preferred for plots and schematics.
