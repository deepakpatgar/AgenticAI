document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("[data-hotel-form]");
  const nightlyRateSelect = document.querySelector("[data-room-select]");
  const nightsInput = document.querySelector("[data-nights]");
  const quantityInputs = Array.from(document.querySelectorAll("[data-qty]"));
  const serviceInputs = Array.from(document.querySelectorAll("[data-service]"));

  const roomTotalEl = document.querySelector("[data-room-total]");
  const menuTotalEl = document.querySelector("[data-menu-total]");
  const serviceTotalEl = document.querySelector("[data-service-total]");
  const taxTotalEl = document.querySelector("[data-tax-total]");
  const serviceChargeTotalEl = document.querySelector("[data-service-charge-total]");
  const grandTotalEl = document.querySelector("[data-grand-total]");
  const liveSummaryEl = document.querySelector("[data-live-summary]");

  if (!form || !nightlyRateSelect || !nightsInput) {
    return;
  }

  const money = (value) => `$${value.toFixed(2).replace(/\.00$/, "")}`;

  const updateQuote = () => {
    const selectedOption = nightlyRateSelect.selectedOptions[0];
    const nightlyRate = Number(selectedOption?.dataset.nightlyRate || 0);
    const nights = Math.max(Number(nightsInput.value || 1), 1);

    const roomTotal = nightlyRate * nights;
    const menuTotal = quantityInputs.reduce((sum, input) => {
      const quantity = Math.max(Number(input.value || 0), 0);
      const unitPrice = Number(input.dataset.unitPrice || 0);
      return sum + quantity * unitPrice;
    }, 0);

    const serviceTotal = serviceInputs.reduce((sum, input) => {
      return sum + (input.checked ? Number(input.dataset.servicePrice || 0) : 0);
    }, 0);

    const subtotal = roomTotal + menuTotal + serviceTotal;
    const tax = subtotal * 0.12;
    const serviceCharge = subtotal * 0.08;
    const total = subtotal + tax + serviceCharge;

    if (roomTotalEl) roomTotalEl.textContent = money(roomTotal);
    if (menuTotalEl) menuTotalEl.textContent = money(menuTotal);
    if (serviceTotalEl) serviceTotalEl.textContent = money(serviceTotal);
    if (taxTotalEl) taxTotalEl.textContent = money(tax);
    if (serviceChargeTotalEl) serviceChargeTotalEl.textContent = money(serviceCharge);
    if (grandTotalEl) grandTotalEl.textContent = money(total);

    if (liveSummaryEl) {
      liveSummaryEl.textContent = `${nights} night${nights === 1 ? "" : "s"} at ${selectedOption?.textContent?.trim() || "your chosen room"} keeps the estimated total at ${money(total)}.`;
    }
  };

  form.addEventListener("input", updateQuote);
  form.addEventListener("change", updateQuote);
  updateQuote();
});
