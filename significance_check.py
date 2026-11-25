"""Do mobile and desktop visitors buy at different rates? Two-proportion z-test.

Run twice:
  1. All visitors per device (query 02). A visitor who used both a phone and a
     computer appears in both groups, which breaks the test's independence assumption.
  2. Single-device visitors only (query 06). Each visitor is in exactly one group.
"""
from math import erf, sqrt


def z_test(name, d_buyers, d_visitors, m_buyers, m_visitors):
    p_d, p_m = d_buyers / d_visitors, m_buyers / m_visitors
    pooled = (d_buyers + m_buyers) / (d_visitors + m_visitors)
    se = sqrt(pooled * (1 - pooled) * (1 / d_visitors + 1 / m_visitors))
    z = (p_m - p_d) / se
    p_value = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))  # two-sided
    verdict = "significant" if p_value < 0.05 else "not significant"
    print(f"{name}\n  Desktop {p_d:.3%} of {d_visitors:,}  |  Mobile {p_m:.3%} of {m_visitors:,}"
          f"\n  z = {z:.2f}, p-value = {p_value:.3f}  ->  {verdict} at 0.05\n")


z_test("1. All visitors per device (overlap included)", 2541, 157079, 1851, 107981)
z_test("2. Single-device visitors only (each visitor counted once)", 2168, 153067, 1485, 104030)
print("Multi-device visitors: 4,168, of whom 665 bought "
      f"({665 / 4168:.1%}), excluded from test 2.")
