import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import HeroSection from '../HeroSection.vue'

describe('HeroSection redesigned UI', () => {
  it('presents the product-focused hero and still emits parsed URLs', async () => {
    const wrapper = mount(HeroSection, {
      props: {
        loading: false,
        compact: false,
        showSlogan: true,
      },
    })

    expect(wrapper.text()).toContain('Agent_video')
    expect(wrapper.text()).toContain('Agent 视频工作台')
    expect(wrapper.text()).toContain('内容章节')
    expect(wrapper.text()).toContain('关键片段')
    expect(wrapper.text()).toContain('粘贴视频链接')

    await wrapper.find('#video-url-input').setValue('https://bilibili.com/video/BV1GJ411x7h7')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('parse')?.[0]).toEqual(['https://www.bilibili.com/video/BV1GJ411x7h7'])
  })
})
