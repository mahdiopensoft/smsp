import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    show: false,
    message: '',
    color: 'success', // 'success', 'error', 'warning', 'info'
    timeout: 4000,
    // Rich notification properties
    title: '',
    avatar: '',
    onClick: null,
    chatId: null,
  }),
  actions: {
    showToast (message, color = 'success', timeout = 4000) {
      if (this.show) {
        this.show = false
        setTimeout(() => {
          this.message = message
          this.color = color
          this.timeout = timeout
          this.title = ''
          this.avatar = ''
          this.onClick = null
          this.chatId = null
          this.show = true
        }, 150)
      } else {
        this.message = message
        this.color = color
        this.timeout = timeout
        this.title = ''
        this.avatar = ''
        this.onClick = null
        this.chatId = null
        this.show = true
      }
    },
    showInteractiveToast ({ title, message, avatar, color = 'info', timeout = 6000, onClick = null, chatId = null }) {
      if (this.show) {
        this.show = false
        setTimeout(() => {
          this.title = title || ''
          this.message = message || ''
          this.avatar = avatar || ''
          this.color = color
          this.timeout = timeout
          this.onClick = onClick
          this.chatId = chatId
          this.show = true
        }, 150)
      } else {
        this.title = title || ''
        this.message = message || ''
        this.avatar = avatar || ''
        this.color = color
        this.timeout = timeout
        this.onClick = onClick
        this.chatId = chatId
        this.show = true
      }
    },
    showSuccess (message, timeout = 4000) {
      this.showToast(message, 'success', timeout)
    },
    showError (message, timeout = 6000) {
      this.showToast(message, 'error', timeout)
    },
    showWarning (message, timeout = 5000) {
      this.showToast(message, 'warning', timeout)
    },
    showInfo (message, timeout = 4000) {
      this.showToast(message, 'info', timeout)
    },
    closeToast () {
      this.show = false
    },
  },
})
