/**
 * Platform Sync API
 * Calls server push endpoints to trigger synchronization
 */
import api from '../../../plugins/axios-plugin'

const SYNC_BASE = '/platform-sync/server'
const PUSH_TIMEOUT = 120_000  // 2 minutes — push iterates all systems with retries

export default {
    /**
     * Push superusers to all sub-systems
     */
    pushSuperUsers(controller) {
        return api.post(`${SYNC_BASE}/superuser/push/`, null, { timeout: PUSH_TIMEOUT ,signal:controller.signal})
    },

    /**
     * Push organizations to all sub-systems
     */
    pushOrganizations(controller) {
        return api.post(`${SYNC_BASE}/organization/push/`, null, { timeout: PUSH_TIMEOUT,signal:controller.signal })
    },

    /**
     * Push user types to all sub-systems
     */
    pushUserTypes(controller) {
        return api.post(`${SYNC_BASE}/usertype/push/`, null, { timeout: PUSH_TIMEOUT ,signal:controller.signal})
    },

    /**
     * Push groups to all sub-systems
     */
    pushGroups(controller) {
        return api.post(`${SYNC_BASE}/group/push/`, null, { timeout: PUSH_TIMEOUT ,signal:controller.signal})
    },

    /**
     * Push all entity types at once (sequential calls)
     */
    async pushAll() {
        const results = {}
        results.userTypes = await this.pushUserTypes()
        results.groups = await this.pushGroups()
        results.organizations = await this.pushOrganizations()
        results.superUsers = await this.pushSuperUsers()
        return results
    },

    /**
     * Get ObjectSync status records (paginated)
     * @param {Object} params - { page, page_size, object_type, search }
     */
    getStatus(params={} , object_type ) {
        
        return api.get('/platform-sync/status/',  {params:{...params.params,object_type}} )
    },
}
