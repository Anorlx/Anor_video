import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import AppHeader from '../AppHeader.vue'

describe('AppHeader history entry', () => {
  it('shows a history action for logged-in users and emits open-history', async () => {
    const wrapper = mount(AppHeader, {
      props: {
        user: {
          email: 'history@example.com',
        },
      },
    })

    await wrapper.find('button').trigger('click')
    const historyButton = wrapper.find('[data-testid="open-history"]')
    expect(historyButton.exists()).toBe(true)

    await historyButton.trigger('click')
    expect(wrapper.emitted('open-history')).toHaveLength(1)
  })

  it('does not show membership upsells or vip status for logged-in users', () => {
    const wrapper = mount(AppHeader, {
      props: {
        user: {
          email: 'free@example.com',
        },
      },
    })

    expect(wrapper.text()).not.toContain('VIP')
    expect(wrapper.text()).not.toContain('会员')
    expect(wrapper.emitted('open-vip')).toBeUndefined()
  })
})
