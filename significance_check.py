"""Is mobile's purchase rate really higher than desktop's? Two-proportion z-test."""
from math import erf, sqrt

desktop_buyers, desktop_visitors = 2541, 157079
mobile_buyers, mobile_visitors = 1851, 107981

p_d = desktop_buyers / desktop_visitors
p_m = mobile_buyers / mobile_visitors
pooled = (desktop_buyers + mobile_buyers) / (desktop_visitors + mobile_visitors)
se = sqrt(pooled * (1 - pooled) * (1 / desktop_visitors + 1 / mobile_visitors))
z = (p_m - p_d) / se
p_value = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))  # two-sided

print(f"Desktop purchase rate: {p_d:.3%}")
print(f"Mobile purchase rate:  {p_m:.3%}")
print(f"z = {z:.2f}, p-value = {p_value:.3f}")
print("Significant at 0.05" if p_value < 0.05 else "Not significant at 0.05: no clear difference")
