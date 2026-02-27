module.exports = {
  "*.ts": [() => "npm run build", "npm run lint:fix", "npm run prettier:fix"],
};
