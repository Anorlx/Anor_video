import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import HistoryPage from '../HistoryPage.vue'

describe('HistoryPage', () => {
  it('renders history items and emits reparse for a selected record', async () => {
    const wrapper = mount(HistoryPage, {
      props: {
        items: [
          {
            id: 1,
            title: 'VueConf Talk',
            platform: 'youtube',
            source_url: 'https://youtu.be/vueconf',
            thumbnail: '',
            uploader: 'Vue Team',
            duration_string: '12:34',
            parsed_at: '2026-04-16T12:00:00+00:00',
          },
        ],
        loading: false,
        loadingMore: false,
        hasMore: false,
        error: '',
      },
    })

    expect(wrapper.text()).toContain('VueConf Talk')
    await wrapper.find('[data-testid="reparse-history-1"]').trigger('click')
    expect(wrapper.emitted('reparse')).toEqual([['https://youtu.be/vueconf']])
  })

  it('renders the empty state when there is no history', () => {
    const wrapper = mount(HistoryPage, {
      props: {
        items: [],
        loading: false,
        loadingMore: false,
        hasMore: false,
        error: '',
      },
    })

    expect(wrapper.text()).toContain('你还没有解析记录')
  })

  it('emits load-more when more history is available', async () => {
    const wrapper = mount(HistoryPage, {
      props: {
        items: [
          {
            id: 3,
            title: 'Load More Video',
            platform: 'youtube',
            source_url: 'https://youtu.be/more',
            thumbnail: '',
            uploader: 'Uploader',
            duration_string: '03:21',
            parsed_at: '2026-04-16T12:00:00+00:00',
          },
        ],
        loading: false,
        loadingMore: false,
        hasMore: true,
        error: '',
      },
    })

    await wrapper.find('[data-testid="load-more-history"]').trigger('click')
    expect(wrapper.emitted('load-more')).toHaveLength(1)
  })

  it('copies the link through navigator.clipboard', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    Object.assign(navigator, { clipboard: { writeText } })

    const wrapper = mount(HistoryPage, {
      props: {
        items: [
          {
            id: 2,
            title: 'Bili Video',
            platform: 'bilibili',
            source_url: 'https://www.bilibili.com/video/BV1',
            thumbnail: '',
            uploader: 'UP 主',
            duration_string: '01:23',
            parsed_at: '2026-04-16T12:00:00+00:00',
          },
        ],
        loading: false,
        loadingMore: false,
        hasMore: false,
        error: '',
      },
    })

    await wrapper.find('[data-testid="copy-history-2"]').trigger('click')
    expect(writeText).toHaveBeenCalledWith('https://www.bilibili.com/video/BV1')
    expect(wrapper.text()).toContain('已复制链接')
  })
})
