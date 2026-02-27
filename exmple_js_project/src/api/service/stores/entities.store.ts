type TrackParams = Array<string | undefined | null> | string;

export class EntitiesStore {
  private entities = {
    orders: new Set<string>(),
    customers: new Set<string>(),
    products: new Set<string>(),
  };

  private track(type: keyof typeof this.entities, ids: TrackParams): void {
    const mappedIds = typeof ids === "string" ? [ids] : ids;

    mappedIds.forEach((id) => {
      if (id) this.entities[type].add(id);
    });
  }

  trackOrders(ids: TrackParams): void {
    this.track("orders", ids);
  }

  trackCustomers(ids: TrackParams): void {
    this.track("customers", ids);
  }

  trackProducts(ids: TrackParams): void {
    this.track("products", ids);
  }

  getOrderIds(): string[] {
    return [...this.entities.orders];
  }

  getCustomerIds(): string[] {
    return [...this.entities.customers];
  }

  getProductIds(): string[] {
    return [...this.entities.products];
  }

  clear(): void {
    Object.values(this.entities).forEach((set) => set.clear());
  }
}
