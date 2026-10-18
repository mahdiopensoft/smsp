/**
 * Web Audio API Sound Synthesizer
 * Provides high-fidelity synthesized notification sounds and call ringtones.
 * Fully offline-capable, highly responsive, and bypasses corporate network blocks.
 */

class AudioSynthesizer {
  constructor () {
    this.ctx = null
    this.activeRingtoneInterval = null
  }

  init () {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)()
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume()
    }
  }

  /**
   * Synthesizes a crisp, clear digital ping sound
   */
  playPing () {
    try {
      this.init()
      const now = this.ctx.currentTime

      const osc = this.ctx.createOscillator()
      const gain = this.ctx.createGain()

      osc.type = 'sine'
      osc.frequency.setValueAtTime(1200, now)

      gain.gain.setValueAtTime(0.25, now)
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3)

      osc.connect(gain)
      gain.connect(this.ctx.destination)

      osc.start(now)
      osc.stop(now + 0.3)
    } catch (e) {
      console.warn('AudioSynthesizer: Ping synthesis failed', e)
    }
  }

  /**
   * Synthesizes a beautiful dual-tone, slightly offset major third iPhone note chime
   */
  playNote () {
    try {
      this.init()
      const now = this.ctx.currentTime

      // Frequencies: C6 (1046.50 Hz) & E6 (1318.51 Hz) - bright major third
      const osc1 = this.ctx.createOscillator()
      const osc2 = this.ctx.createOscillator()
      const gain1 = this.ctx.createGain()
      const gain2 = this.ctx.createGain()

      osc1.type = 'sine'
      osc1.frequency.setValueAtTime(1046.50, now)
      gain1.gain.setValueAtTime(0.18, now)
      gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.4)

      osc2.type = 'sine'
      osc2.frequency.setValueAtTime(1318.51, now)
      gain2.gain.setValueAtTime(0.18, now + 0.05)
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.45)

      osc1.connect(gain1)
      gain1.connect(this.ctx.destination)

      osc2.connect(gain2)
      gain2.connect(this.ctx.destination)

      osc1.start(now)
      osc1.stop(now + 0.45)

      osc2.start(now + 0.05) // Strum effect
      osc2.stop(now + 0.5)
    } catch (e) {
      console.warn('AudioSynthesizer: Note chime synthesis failed', e)
    }
  }

  /**
   * Synthesizes a gorgeous signature three-note marimba rising triad
   */
  playMarimba () {
    try {
      this.init()
      const now = this.ctx.currentTime

      const playStrike = (freq, time, duration) => {
        const osc = this.ctx.createOscillator()
        const gain = this.ctx.createGain()

        osc.type = 'triangle'
        osc.frequency.setValueAtTime(freq, time)

        gain.gain.setValueAtTime(0.2, time)
        gain.gain.exponentialRampToValueAtTime(0.001, time + duration)

        osc.connect(gain)
        gain.connect(this.ctx.destination)

        osc.start(time)
        osc.stop(time + duration)
      }

      // Rising triad: G5 (783.99 Hz), C6 (1046.50 Hz), E6 (1318.51 Hz)
      playStrike(783.99, now, 0.25)
      playStrike(1046.50, now + 0.08, 0.3)
      playStrike(1318.51, now + 0.16, 0.4)
    } catch (e) {
      console.warn('AudioSynthesizer: Marimba synthesis failed', e)
    }
  }

  /**
   * Starts a repeating synthesized ringtone for incoming calls
   */
  startRingtone () {
    this.stopRingtone()
    this.playMarimba() // First strike instantly

    this.activeRingtoneInterval = setInterval(() => {
      this.playMarimba()
    }, 1500)
  }

  /**
   * Stops the active repeating synthesized ringtone
   */
  stopRingtone () {
    if (this.activeRingtoneInterval) {
      clearInterval(this.activeRingtoneInterval)
      this.activeRingtoneInterval = null
    }
  }

  /**
   * Play a realistic telephone dialing tone strike (US/Middle East dual-tone 440Hz + 480Hz)
   */
  playDialingToneStrike (time, duration) {
    try {
      this.init()
      const now = time || this.ctx.currentTime

      const osc1 = this.ctx.createOscillator()
      const osc2 = this.ctx.createOscillator()
      const gain = this.ctx.createGain()

      osc1.type = 'sine'
      osc1.frequency.setValueAtTime(440, now)

      osc2.type = 'sine'
      osc2.frequency.setValueAtTime(480, now)

      // Soft volume for comfortable dialing sound
      gain.gain.setValueAtTime(0.08, now)
      gain.gain.exponentialRampToValueAtTime(0.08, now + duration - 0.1)
      gain.gain.exponentialRampToValueAtTime(0.001, now + duration)

      osc1.connect(gain)
      osc2.connect(gain)
      gain.connect(this.ctx.destination)

      osc1.start(now)
      osc1.stop(now + duration)
      osc2.start(now)
      osc2.stop(now + duration)

      this.activeOscillators = this.activeOscillators || []
      this.activeOscillators.push(osc1, osc2)
    } catch (e) {
      console.warn('AudioSynthesizer: Dialing tone synthesis failed', e)
    }
  }

  startDialingTone () {
    this.init() // Ensure AudioContext is initialized!
    this.stopDialingTone()
    this.activeOscillators = []

    const playNext = () => {
      if (this.ctx) {
        this.playDialingToneStrike(this.ctx.currentTime, 1.5)
      }
    }

    playNext()
    this.activeDialingInterval = setInterval(playNext, 4000) // Repeat every 4 seconds
  }

  /**
   * Stops the active synthesized dialing tone
   */
  stopDialingTone () {
    if (this.activeDialingInterval) {
      clearInterval(this.activeDialingInterval)
      this.activeDialingInterval = null
    }
    if (this.activeOscillators) {
      this.activeOscillators.forEach(osc => {
        try {
          osc.stop()
        } catch (e) {}
      })
      this.activeOscillators = []
    }
  }
}

export const audioSynthesizer = new AudioSynthesizer()
export default audioSynthesizer
