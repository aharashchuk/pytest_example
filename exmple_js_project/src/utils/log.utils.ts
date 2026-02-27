export function log(message: string) {
  if (process.env.TEST_ENV) {
    console.log(message);
  }
}
