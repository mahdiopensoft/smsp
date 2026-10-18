import api from "../../../plugins/axios-plugin";

/**
 * Hybrid BFF Authentication API
 * No refresh tokens in frontend
 */
export const authApi = {
  /**
   * Login
   * Backend sets HttpOnly refresh cookie
   */
  async login(username, password) {
    const response = await api.post("auth/token/", {
      username,
      password,
    });

    return response.data;
  },

  /**
   * Refresh session
   * NO refresh token sent from frontend
   * Backend reads HttpOnly cookie
   */
  async refreshToken() {
    const response = await api.post("/auth/token/refresh",{},{
        skipInterceptor:true,
        timeout:5000
    });
    

    return response.data;
  },

  /**
   * Logout
   * Backend clears HttpOnly cookie + revokes session
   */
  async logout() {
 
    try {
      await api.post("/auth/logout/",);
    } catch (error) {
      console.warn("Logout API error:", error);
    }
  },

  /**
   * Get current user profile
   */
  async getProfile() {
    const response = await api.get("/auth/profile/");

    return response.data;
  },

  /**
   * Update profile
   */
  async updateProfile(data) {
    const response = await api.put("/auth/profile/", data);

    return response.data;
  },

  /**
   * Change password
   */
  async changePassword(oldPassword, newPassword) {
    const response = await api.post("/auth/profile/change-password/", {
      old_password: oldPassword,
      new_password: newPassword,
    });

    return response.data;
  },
};

export default authApi;
