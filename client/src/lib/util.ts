const tryFormatter = new Intl.NumberFormat("tr-TR", {
  style: "currency",
  currency: "TRY",
});

export function formatCurrency(kurus: number) {
  return tryFormatter.format(kurus / 100); // 20000 → "₺200,00"
}
