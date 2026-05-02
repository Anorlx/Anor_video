import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import App from '../App.vue'

vi.mock('../api/video.js', () => ({
  parseVideo: vi.fn(),
  downloadViaServer: vi.fn(),
}))

vi.mock('../api/history.js', () => ({
  fetchHistory: vi.fn(),
}))

vi.mock('../api/auth.js', () => ({
  getSavedUser: vi.fn(() => null),
  fetchMe: vi.fn(),
  logout: vi.fn(),
  isLoggedIn: vi.fn(() => false),
}))

describe('App homepage cleanup', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
  })

  it('does not show pricing, platform grids, or a price navigation item on the homepage', async () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          Teleport: true,
          HeroSection: { template: '<div data-testid="hero-section">hero</div>' },
          FeatureSection: true,
          HowToSection: true,
          ComparisonSection: true,
          AppFooter: true,
          AuthModal: true,
          HistoryPage: true,
        },
      },
    })

    await flushPromises()

    expect(wrapper.find('[data-testid="pricing-section"]').exists()).toBe(false)
    expect(wrapper.find('[data-testid="platform-section"]').exists()).toBe(false)
    expect(wrapper.find('a[href="#pricing"]').exists()).toBe(false)
  })
})
