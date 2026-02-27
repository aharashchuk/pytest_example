import { test } from "@playwright/test";

export function logStep<This, Args extends unknown[], Return>(message?: string) {
  return function actualDecorator(
    target: (this: This, ...args: Args) => Promise<Return>,
    context: ClassMethodDecoratorContext<This, (this: This, ...args: Args) => Promise<Return>>,
  ) {
    function replacementMethod(this: This, ...args: Args): Promise<Return> {
      const ctor = this as unknown as { constructor: { name: string } };
      const name = message ?? `${ctor.constructor.name}.${String(context.name)}`;
      return test.step(name, async () => target.call(this, ...args), {
        box: false,
      });
    }
    return replacementMethod;
  };
}
