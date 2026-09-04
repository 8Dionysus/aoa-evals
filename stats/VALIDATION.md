# Stats Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
rg -N '^status: ' evals -g 'eval.yaml' | sort
python scripts/validate_local_stats_port.py
```
