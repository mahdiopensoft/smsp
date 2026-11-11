/**
 * MFA (Multi-Factor Authentication) API
 * Endpoints: /user-manager/mfa/
 */
import api from "../../../plugins/axios-plugin";

const MFA_BASE = "/user-manager/mfa";

export const mfaApi = {
  /**
   * Get MFA status for current user
   * @returns {Promise} { is_enabled, backup_codes_remaining }
   */
  async getStatus() {
    const response = await api.get(`${MFA_BASE}/status/`);
    return response.data;
  },

  /**
   * Setup MFA — returns QR code and secret
   * @returns {Promise} { secret_key, qr_code_base64, provisioning_uri }
   */
  async setup() {
    const response = await api.post(`${MFA_BASE}/setup/`);
    return response.data;
  },

  /**
   * Verify OTP and enable MFA
   * @param {string} otpCode — 6-digit code from authenticator app
   * @returns {Promise} { backup_codes: [...] }
   */
  async verifyAndEnable(otpCode) {
    const response = await api.post(`${MFA_BASE}/verify/`, {
      otp_code: otpCode,
    });
    return response.data;
  },

  /**
   * Disable MFA (requires valid OTP)
   * @param {string} otpCode
   * @returns {Promise}
   */
  async disable(otpCode) {
    const response = await api.post(`${MFA_BASE}/disable/`, {
      otp_code: otpCode,
    });
    return response.data;
  },

  /**
   * Verify OTP during login (second factor)
   * @param {string} username
   * @param {string} otpCode
   * @returns {Promise} { access, refresh }
   */
  async loginVerify(username, otpCode) {
    const response = await api.post(`${MFA_BASE}/login/`, {
      username,
      otp_code: otpCode,
    });
    return response.data;
  },
};

export default mfaApi;
