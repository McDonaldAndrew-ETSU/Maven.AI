import dotenv from 'dotenv';
import fs from 'fs/promises';
import { expect, test } from '@playwright/test';

dotenv.config({ path: '../.env' });

test('Maven.AI Interactor', async ({ page }) => {
	await page.goto(process.env.URL);

	let incrementor = 1;
	while (true) {
		await expect(page.locator(process.env.LOCATOR_ID).first()).toBeVisible({
			timeout: 10_000
		});

		for (const locator of await page.locator(process.env.LOCATOR_ID).all()) {
			const text = await locator.innerText();

			await fs.appendFile(`../test_data/${process.env.TEST_DATA}`, `${text}\n`);
		}

		try {
			await expect(page.getByLabel(`page ${++incrementor}`)).toBeVisible({
				timeout: 500
			});
			await page.getByLabel(`page ${incrementor}`).click();
		} catch (e) {
			return false;
		}
	}
});
