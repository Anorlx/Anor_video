import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import App from '../App.vue'

const { mockUser, parseVideo, fetchHistory, fetchMe } = vi.hoisted(() => {
  const mockUser = {
    email: 'history@example.com',
    is_vip: true,
    vip_expire_at: '2099-12-31T23:59:59+00:00',
  }

  return {
    mockUser,
    parseVideo: vi.fn().mockResolvedValue({
      success: true,
      data: {
        title: 'Reparsed Video',
        uploader: 'Uploader',
        platform: 'youtube',
        thumbnail: '',
        formats: [],
      },
    }),
    fetchHistory: vi.fn().mockResolvedValue({
      success: true,
      data: {
        items: [
          {
            id: 1,
            title: 'History Entry',
            source_url: 'https://youtu.be/history-entry',
          },
        ],
        total: 1,
        has_more: false,
      },
    }),
    fetchMe: vi.fn().mockResolvedValue(mockUser),
  }
})

vi.mock('../api/video.js', () => ({
  parseVideo,
  downloadViaServer: vi.fn(),
}))

vi.mock('../api/history.js', () => ({
  fetchHistory,
}))

vi.mock('../api/payment.js', () => ({
  createCheckoutSession: vi.fn(),
}))

vi.mock('../api/auth.js', () => ({
  getSavedUser: vi.fn(() => mockUser),
  fetchMe,
  logout: vi.fn(),
  isLoggedIn: vi.fn(() => true),
}))

describe('App history flow', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    window.history.replaceState({}, '', '/')
  })

  it('loads history from the header and reparses a selected history record', async () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          Teleport: true,
          AppHeader: {
            props: ['user'],
            template: `
              <button data-testid="open-history-from-header" @click="$emit('open-history')">
                history
              </button>
            `,
          },
          HeroSection: { template: '<div data-testid="hero-section">hero</div>' },
          VideoResult: true,
          VideoSummary: true,
          FeatureSection: true,
          HowToSection: true,
          ComparisonSection: true,
          AppFooter: true,
          AuthModal: true,
          HistoryPage: {
            props: ['items'],
            template: `
              <div data-testid="history-page">
                <span>{{ items.length }}</span>
                <button
                  data-testid="reparse-history-item"
                  @click="$emit('reparse', items[0].source_url)"
                >
                  reparse
                </button>
              </div>
            `,
          },
        },
      },
    })

    await flushPromises()

    await wrapper.find('[data-testid="open-history-from-header"]').trigger('click')
    await flushPromises()

    expect(fetchHistory).toHaveBeenCalledWith({ offset: 0, limit: 20 })
    expect(wrapper.find('[data-testid="history-page"]').exists()).toBe(true)

    await wrapper.find('[data-testid="reparse-history-item"]').trigger('click')
    await flushPromises()

    expect(parseVideo).toHaveBeenCalledWith('https://youtu.be/history-entry')
  })
})
