import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import AppHeader from '../AppHeader.vue'

describe('AppHeader history entry', () => {
  it('shows a history action for logged-in users and emits open-history', async () => {
    const wrapper = mount(AppHeader, {
      props: {
        user: {
          email: 'history@example.com',
          is_vip: true,
          vip_expire_at: '2099-12-31T23:59:59+00:00',
        },
      },
    })

    await wrapper.find('button').trigger('click')
    const historyButton = wrapper.find('[data-testid="open-history"]')
    expect(historyButton.exists()).toBe(true)

    await historyButton.trigger('click')
    expect(wrapper.emitted('open-history')).toHaveLength(1)
  })
})
