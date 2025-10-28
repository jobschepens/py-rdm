# Quick Reference: Feedback vs Affirmation Analysis

## 🎯 Main Finding
**Affirmations have HIGHER velocity and amplitude than feedback gestures.**

---

## 📊 Results at a Glance

### Significant Differences by Language

| Language | Length | Amplitude | Velocity |
|----------|--------|-----------|----------|
| **DGS (German Sign)** | ✅ FB > AF (small) | ❌ | ✅ AF > FB (medium) |
| **GER (German Spoken)** | ❌ | ✅ AF > FB **(LARGE)** | ✅ AF > FB **(LARGE)** |
| **RSL (Russian Sign)** | ❌ | ✅ AF > FB (small) | ✅ AF > FB (small) |
| **RUS (Russian Spoken)** | ❌ | ❌ | ❌ |

### Sample Sizes (Affirmation groups)
- DGS: n=88-91 ✅ Good
- GER: n=45-46 ✅ Acceptable  
- RSL: n=34-39 ✅ Acceptable
- RUS: n=27-29 ⚠️ Marginal (underpowered)

---

## 🔬 Methods
- **Test:** Mann-Whitney U (non-parametric)
- **Why not t-test?** 100% of distributions are non-normal
- **Outliers:** Removed using IQR method

---

## ⚠️ Key Limitations
1. Small affirmation samples (2-13% of data)
2. RUS_2503 likely underpowered
3. Unequal group sizes reduce power
4. Cannot separate language from modality effects

---

## ✅ Confidence Ratings

| Finding | Confidence |
|---------|-----------|
| GER differences | ⭐⭐⭐⭐⭐ Very High |
| DGS velocity | ⭐⭐⭐⭐⭐ Very High |
| RSL differences | ⭐⭐⭐ Medium |
| RUS differences | ⭐ Low (underpowered) |

---

## 📝 Reporting Checklist
- [x] Mann-Whitney U test used
- [x] Effect sizes reported (Cohen's d)
- [x] Non-normal distributions documented
- [x] Sample size limitations acknowledged
- [x] Outliers removed systematically
- [ ] Consider adding confidence intervals
- [ ] Acknowledge power limitations in discussion

---

## 💡 Key Insights
1. **German speakers** differentiate affirmation/feedback most strongly
2. **Velocity** is the most consistent differentiator (3/4 languages)
3. **Duration** doesn't differ between gesture types
4. **Effect sizes** range from negligible (d=0.03) to very large (d=1.19)

---

## 🔮 Recommendations
1. ✅ Use Mann-Whitney U results (appropriate test)
2. ⚠️ Interpret RUS_2503 results cautiously
3. 🔬 Collect more affirmation data for future studies
4. 📊 Report both effect sizes AND p-values
5. 📝 Mention sample size limitations in discussion

---

**Files Generated:**
- `SUMMARY_REPORT.md` - Full detailed report (this file)
- `feedback_affirmation_analysis_results.csv` - All statistical results
- `sample_size_assessment.csv` - Power analysis results
- `test_comparison_results.csv` - Test comparison data
- Various `.png` files - Visualizations

**Date:** October 13, 2025
