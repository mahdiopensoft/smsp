<template>
  <div fluid class="pa-0 main-pulse-layout">
    <div class="glass-orb orb-1"></div>
    <div class="glass-orb orb-2"></div>
    <div class="glass-orb orb-3"></div>

    <!-- Main Content Stage -->
    <v-container fluid class="pa-6 pa-md-8 pb-md-2 position-relative" style="z-index: 1">
      <!-- Global Health Matrix -->
      <v-row class="mb-10">
        <v-col
          v-for="(metric, idx) in metricCards"
          :key="idx"
          cols="12"
          sm="6"
          md="3"
          class="pt-0"
        >
          <div
            class="health-matrix-node"
            :class="metric.colorClass"
            :style="{ animationDelay: idx * 100 + 'ms' }"
          >
            <div class="node-glow"></div>
            <div class="node-content">
              <div class="d-flex justify-space-between align-start mb-5">
                <div class="text-overline metric-label">
                  {{ metric.label }}
                </div>
                <div class="metric-icon-box" :class="metric.colorClass">
                  <v-icon size="20" :icon="metric.icon" color="white"></v-icon>
                </div>
              </div>

              <div class="d-flex align-end justify-space-between">
                <div class="d-flex align-baseline">
                  <div
                    v-if="loading?.groups"
                    class="skeleton-bone"
                    style="width: 60px; height: 32px"
                  ></div>
                  <template v-else>
                    <div class="metric-value">{{ metric.value }}</div>
                    <div
                      class="text-body-2 ms-1 opacity-40 font-weight-bold"
                      v-if="metric.suffix"
                    >
                      {{ metric.suffix }}
                    </div>
                  </template>
                </div>

                <div
                  v-if="metric.key === 'totalScreens'"
                  class="d-flex align-center gap-2"
                >
                  <!-- <v-chip
                    size="x-small"
                    color="primary"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    {{ metric.unsyncedCount }} New
                  </v-chip> -->
                  <v-btn
                    variant="tonal"
                    size="x-small"
                    color="primary"
                    icon
                    @click="syncAllNewScreens"
                    :disabled="loading?.groups && !loading?.sync_screen"
                    :loading="loading?.sync_screen"
                    class="sync-pulse-btn"
                  >
                    <v-icon icon="mdi-sync" size="16"></v-icon>
                    <v-tooltip activator="parent" location="top">{{
                      $t("syncNewScreens")
                    }}</v-tooltip>
                  </v-btn>
                </div>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
      <!-- Logic groups Stage -->
      <v-row>
        <v-col cols="12">
          <div
            class="section-title-premium d-flex align-center justify-space-between mt-0"
          >
            <div class="d-flex align-center">
              <div class="section-accent me-3"></div>
              <div>
                <h2 class="text-h5 font-weight-black">
                  {{ $t("activePipelinesTitle") }}
                </h2>
                <p class="text-caption opacity-40 font-weight-medium mb-0">
                  {{
                    sync_groups?.length !== 1
                      ? $t("pipelinesActive", { count: sync_groups?.length })
                      : $t("pipelineActive", { count: sync_groups?.length })
                  }}
                </p>
              </div>
            </div>
            <!-- Global Search Location -->
            <v-text-field
              v-model="searchInput"
              variant="solo"
              density="compact"
              :placeholder="$t('searchPlaceholder')"
              prepend-inner-icon="mdi-magnify"
              append-inner-icon="mdi-keyboard-return"
              clearable
              hide-details
              class="global-pipelines-search flex-grow-1 mr-6"
              style="max-width: 400px; border-radius: 14px; overflow: hidden"
              :loading="loading?.groups"
              @keyup.enter="handleSearch"
              @click:clear="handleClearSearch"
            >
              <v-tooltip activator="append-inner" location="top">{{
                $t("pressEnterToSearch")
              }}</v-tooltip>
            </v-text-field>
            <div class="d-flex gap-3">
              <v-btn
                variant="tonal"
                color="primary"
                class="action-btn-premium group-btn-primary"
                @click="(showAddGroup = true), (group_data = {})"
              >
                <v-icon icon="mdi-plus" start></v-icon>
                {{ $t("newPipeline") }}
              </v-btn>
            </div>
          </div>
        </v-col>

        <!-- Skeleton groups Cards (loading state) -->
        <template v-if="loading?.groups">
          <v-col v-for="n in 3" :key="'skel-group-' + n" cols="12" xl="4" lg="6">
            <div
              class="pipeline-card-glass skeleton-pipeline-card"
              :style="{ animationDelay: (n - 1) * 100 + 'ms' }"
            >
              <div class="pipeline-header pa-5 d-flex align-center">
                <div
                  class="skeleton-bone"
                  style="
                    width: 34px;
                    height: 34px;
                    border-radius: 10px;
                    margin-left: 12px;
                  "
                ></div>
                <div class="flex-grow-1">
                  <div
                    class="skeleton-bone"
                    style="width: 50%; height: 12px; margin-bottom: 8px"
                  ></div>
                  <div class="skeleton-bone" style="width: 30%; height: 8px"></div>
                </div>
              </div>
              <div class="pa-4 d-flex flex-column" style="gap: 8px">
                <div
                  v-for="s in 3"
                  :key="s"
                  class="skeleton-bone"
                  style="width: 100%; height: 44px; border-radius: 12px"
                ></div>
              </div>
              <div class="pipeline-footer pa-4 d-flex justify-end gap-2">
                <div
                  class="skeleton-bone"
                  style="width: 100px; height: 30px; border-radius: 10px"
                ></div>
                <div
                  class="skeleton-bone"
                  style="width: 110px; height: 30px; border-radius: 10px"
                ></div>
              </div>
            </div>
          </v-col>
        </template>
        <v-col
          v-else
          v-for="(group, gIdx) in filteredGroups"
          :key="group?.id"
          cols="12"
          xl="4"
          lg="6"
        >
          <div class="pipeline-card-glass" :style="{ animationDelay: gIdx * 80 + 'ms' }">
            <!-- Pipeline Header -->
            <div class="pipeline-header pa-5 d-flex align-center">
              <div class="pipeline-badge me-3">
                <v-icon icon="mdi-pipe" size="14" color="white"></v-icon>
              </div>
              <div class="flex-grow-1">
                <h3 class="text-subtitle-1 font-weight-black leading-none mb-1">
                  {{ group?.name_ar }}
                </h3>
                <div class="d-flex align-center gap-3">
                  <span class="text-caption opacity-50 font-weight-medium">
                    <v-icon icon="mdi-monitor" size="12" class="ml-1"></v-icon>
                    {{
                      group?.screens?.length !== 1
                        ? $t("screensCount", {
                            count: group?.screens?.length,
                          })
                        : $t("screenCount", {
                            count: group?.screens?.length,
                          })
                    }}
                  </span>
                  <!-- <span
                    v-if="getGroupFailedCount(group) > 0"
                    class="text-caption font-weight-bold failed-count-badge"
                  >
                    <v-icon
                      icon="mdi-alert-circle"
                      size="12"
                      class="me-1"
                    ></v-icon>
                    {{
                      $t("failedCount", { count: getGroupFailedCount(group) })
                    }}
                  </span> -->
                </div>
              </div>
              <div class="d-flex align-center gap-1">
                <v-btn
                  icon
                  variant="text"
                  size="x-small"
                  class="opacity-50 header-action-btn"
                  @click="toggleCompact(group?.id)"
                >
                  <v-icon
                    :icon="
                      !isCompact(group?.id) ? 'mdi-view-headline' : 'mdi-view-sequential'
                    "
                    size="18"
                  ></v-icon>
                  <v-tooltip activator="parent" location="top">{{
                    $t("toggleCompact")
                  }}</v-tooltip>
                </v-btn>
                <v-btn
                  variant="tonal"
                  size="small"
                  color="primary"
                  class="action-btn-premium px-3 ms-1"
                  @click="showBulkScreenDialog(group)"
                >
                  {{ $t("add") }}
                  <v-icon icon="mdi-plus" end size="14"></v-icon>
                </v-btn>
                <v-menu location="bottom end" :close-on-content-click="true">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      icon
                      variant="text"
                      size="x-small"
                      v-bind="props"
                      class="opacity-50 header-action-btn"
                    >
                      <v-icon icon="mdi-dots-vertical" size="18"></v-icon>
                    </v-btn>
                  </template>
                  <v-list class="glass-list-premium" density="compact">
                    <v-list-item
                      prepend-icon="mdi-cloud-upload-outline"
                      :title="$t('uploadAllSeq')"
                      :disabled="isGrroupEmpty(group, 'push')"
                      @click="confirmAndRunGroupSequence(group, 'push')"
                    ></v-list-item>
                    <v-list-item
                      prepend-icon="mdi-cloud-download-outline"
                      :title="$t('downloadAllSeq')"
                      :disabled="isGrroupEmpty(group, 'pull')"
                      @click="confirmAndRunGroupSequence(group, 'pull')"
                    ></v-list-item>
                    <v-divider class="my-1 opacity-10"></v-divider>
                    <v-list-item
                      prepend-icon="mdi-pencil-outline"
                      :title="$t('edit_group')"
                      base-color="success"
                      @click="openEditGroupDialog(group)"
                    ></v-list-item>
                    <v-list-item
                      prepend-icon="mdi-trash-can-outline"
                      :title="$t('deletePipeline')"
                      base-color="error"
                      @click="confirmDeleteGroup(group)"
                    ></v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </div>

            <!-- Pipeline Body -->
            <div
              class="pipeline-body pa-4 custom-scrollbar"
              :class="{ 'is-scrollable': group?.screens?.length > 5 }"
            >
              <!-- Skeleton Loading State -->
              <div
                v-if="loading[`screens_${group?.id}`]"
                class="d-flex flex-column"
                style="gap: 8px"
              >
                <div
                  v-for="n in 3"
                  :key="'skel-' + n"
                  class="skeleton-bone"
                  style="width: 100%; height: 44px; border-radius: 12px"
                ></div>
              </div>
              <draggable
                v-else-if="!isGrroupEmpty(group)"
                :list="group?.screens"
                :group="'group-' + group?.id"
                item-key="screen_id"
                handle=".node-drag-handle"
                class="pipeline-nodes-track"
                @change="onDragChange($event, group)"
              >
                <template #item="{ element, index }">
                  <div
                    v-show="
                      !appliedSearch ||
                      element?.screen
                        ?.toLowerCase()
                        ?.includes(appliedSearch.toLowerCase())
                    "
                    class="logic-node-card"
                    :class="{
                      'is-active': element?.push?.loading || element?.pull?.loading,
                      'is-success': element.status === 2 || element.status === 'success',
                      'is-new-updates': element.status === 3,
                      'is-failed': element.status === 4,
                      'is-compact': isCompact(group?.id),
                    }"
                  >
                    <div class="node-drag-handle">
                      <v-icon
                        size="16"
                        class="opacity-25"
                        icon="mdi-drag-vertical"
                      ></v-icon>
                    </div>
                    <div class="node-id-tag">{{ index + 1 }}</div>

                    <div class="node-main flex-grow-1 mx-3 overflow-hidden">
                      <div class="d-flex align-center">
                        <span class="text-body-2 font-weight-bold text-truncate">{{
                          element?.screen
                        }}</span>
                        <v-chip
                          size="x-small"
                          class="ms-2 type-chip-enhanced"
                          :color="statusScreen[element.status]?.color"
                          :prepend-icon="statusScreen[element.status]?.icon"
                          :class="element?.status_name"
                        >
                          {{ element?.status_name }}
                        </v-chip>
                      </div>
                      <!-- <v-progress-linear
                        :model-value="element?.successRate || 75"
                        height="3"
                        rounded
                        class="node-health-progress"
                        :color="getHealthColor(element?.successRate || 75)"
                        bg-color="transparent"
                      ></v-progress-linear> -->
                    </div>

                    <div class="node-status-indicator me-1">
                      <v-tooltip
                        v-if="element?.sync_error"
                        activator="parent"
                        location="top"
                        open-delay="300"
                      >
                        {{ element?.sync_error }}
                        <template #activator="{ props }">
                          <v-icon
                            v-bind="props"
                            :color="getStatusColor(element.status)"
                            :icon="getStatusIcon(element.status)"
                            size="18"
                          >
                            <!-- :class="{
                              'spin-animation':
                                element?.push?.loading ||
                                element?.pull?.loading,
                            }" -->
                          </v-icon>
                        </template>
                      </v-tooltip>
                      <v-icon
                        v-else
                        v-bind="props"
                        :color="getStatusColor(element.status)"
                        :icon="getStatusIcon(element.status)"
                        size="18"
                      >
                        <!-- :class="{
                          'spin-animation':
                            element?.push?.loading || element?.pull?.loading,
                        }" -->
                      </v-icon>
                    </div>

                    <div class="node-actions d-flex align-center">
                      <v-btn
                        v-if="element?.settings?.can_pull"
                        variant="text"
                        color="secondary"
                        size="x-small"
                        class="node-action-btn"
                        icon
                        @click="syncScreen(element, 'pull')"
                        :loading="element?.pull?.loading"
                      >
                        <v-icon icon="mdi-cloud-download-outline" size="16"></v-icon>
                        <v-tooltip activator="parent" location="top" open-delay="300">
                          {{ $t("download") }}
                        </v-tooltip>
                      </v-btn>
                      <v-btn
                        variant="text"
                        color="secondary"
                        size="x-small"
                        class="node-action-btn"
                        icon
                        @click="
                          OpenDialogSettingEdit(element.group_id, element, 'setting_edit')
                        "
                        :loading="element?.setting_edit?.loading"
                      >
                        <v-icon icon="mdi-cog-outline" size="16"></v-icon>
                        <v-tooltip activator="parent" location="top" open-delay="300">
                          {{ $t("setting_edit") }}
                        </v-tooltip>
                      </v-btn>
                      <v-btn
                        v-if="element?.status != 2"
                        variant="text"
                        color="primary"
                        size="x-small"
                        class="node-action-btn"
                        icon
                        @click="syncScreen(element, 'push')"
                        :loading="element?.push?.loading"
                      >
                        <v-icon icon="mdi-cloud-upload-outline" size="16"></v-icon>
                        <v-tooltip activator="parent" location="top" open-delay="300">
                          {{ $t("upload") }}
                        </v-tooltip>
                      </v-btn>

                      <v-btn
                        variant="text"
                        size="x-small"
                        color="error"
                        class="node-action-btn"
                        icon
                        @click="openScreenDialog(element, group)"
                      >
                        <v-icon icon="mdi-close" size="14"></v-icon>
                        <v-tooltip activator="parent" location="top" open-delay="300">
                          {{ $t("remove_screen") }}
                        </v-tooltip>
                      </v-btn>
                    </div>
                  </div>
                </template>
              </draggable>

              <div v-else-if="isGrroupEmpty(group)" class="empty-pipeline-state">
                <div class="empty-icon-container mb-3">
                  <v-icon size="32" class="opacity-25" icon="mdi-connection"></v-icon>
                </div>
                <div class="text-body-2 opacity-35 font-weight-bold mb-1">
                  {{ $t("noScreensAttached") }}
                </div>
                <div class="text-caption opacity-25 mb-4">
                  {{ $t("addScreensToSync") }}
                </div>
                <v-btn
                  variant="tonal"
                  size="small"
                  color="primary"
                  class="text-none action-btn-premium"
                  @click="showBulkScreenDialog(group)"
                  prepend-icon="mdi-plus"
                >
                  {{ $t("attachScreens") }}
                </v-btn>
              </div>
            </div>

            <!-- Pipeline Footer -->
            <div class="pipeline-footer pa-4 d-flex justify-end align-center">
              <div class="d-flex gap-2 flex-grow-1 justify-end">
                <template
                  v-if="
                    !(loading[`pull_${group?.id}`] || loading[`push_${group?.id}`]) ||
                    stop_group_sequence
                  "
                >
                  <v-btn
                    v-if="!appliedSearch"
                    variant="tonal"
                    size="small"
                    color="secondary"
                    class="action-btn-premium px-4"
                    :loading="loading[`pull_${group?.id}`]"
                    :disabled="isGrroupEmpty(group, 'pull')"
                    @click="confirmAndRunGroupSequence(group, 'pull')"
                  >
                    <v-icon icon="mdi-cloud-download-outline" start size="16"></v-icon>
                    {{ $t("downloadAll") }}
                  </v-btn>
                  <v-btn
                    v-if="!appliedSearch"
                    variant="tonal"
                    size="small"
                    color="primary"
                    class="action-btn-premium px-4"
                    :loading="loading[`push_${group?.id}`]"
                    :disabled="isGrroupEmpty(group, 'push')"
                    @click="confirmAndRunGroupSequence(group, 'push')"
                  >
                    <v-icon icon="mdi-cloud-upload-outline" start size="16"></v-icon>
                    {{ $t("uploadAll") }}
                  </v-btn>
                </template>
                <template v-else>
                  <div class="d-flex w-100 justify-space-between">
                    <div class="d-flex align-center gap-2">
                      <span class="text-caption font-weight-bold opacity-60">{{
                        $t("syncing")
                      }}</span>

                      <v-progress-circular
                        indeterminate
                        size="16"
                        width="2"
                        color="primary"
                      ></v-progress-circular>
                    </div>
                    <v-btn
                      variant="tonal"
                      size="small"
                      color="error"
                      class="action-btn-premium px-4"
                      @click="stop_group_sequence = true"
                    >
                      <v-icon icon="mdi-stop" start size="16"></v-icon>
                      {{ $t("stop") }}
                    </v-btn>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </v-col>

        <v-col cols="12" v-if="!loading?.groups && filteredGroups.length === 0">
          <div class="no-pipelines-empty pa-16 text-center">
            <div class="empty-glow"></div>
            <div class="empty-icon-float mb-6">
              <v-icon size="56" class="opacity-15" icon="mdi-pipe-disconnected"></v-icon>
            </div>
            <h3 class="text-h5 font-weight-black mb-2">
              {{ appliedSearch ? $t("noMatchingPipelines") : $t("noActivePipelines") }}
            </h3>
            <p class="text-body-2 opacity-50 mb-8 mx-auto" style="max-width: 360px">
              {{ appliedSearch ? $t("adjustSearch") : $t("buildFirstWorkflow") }}
            </p>
            <v-btn
              v-if="!appliedSearch"
              variant="tonal"
              size="large"
              color="primary"
              class="action-btn-premium group-btn-primary px-10"
              @click="showAddGroup = true"
            >
              <v-icon icon="mdi-plus" start></v-icon>
              {{ $t("createFirstPipeline") }}
            </v-btn>
            <v-btn
              v-else
              variant="tonal"
              color="primary"
              class="action-btn-premium"
              @click="handleClearSearch"
            >
              <v-icon icon="mdi-close" start></v-icon>
              {{ $t("clearSearch") }}
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Bulk Groups Assignment Dialog -->
    <custom-dialog
      v-model="assignDialog.show"
      width="520"
      height="auto"
      :title="$t('attachScreens')"
    >
      <template v-slot>
        <v-container class="pa-8 py-5">
          <!-- <div class="dialog-header-icon mb-5">
            <v-icon
              :icon="
                assignDialog.mode === 'screen'
                  ? 'mdi-pipe'
                  : 'mdi-monitor-multiple'
              "
              size="24"
              color="white"
            ></v-icon>
          </div> -->
          <!-- <h2 class="">
            {{}}
          </h2> -->
          <!-- Screen Selection (Multi-Add to Group) -->
          <div v-if="assignDialog.mode === 'group'" class="mb-3">
            <auto-list
              v-model="assignDialog.selectedScreens"
              name="parent_screen"
              :label="$t('screens')"
              hideDetails
              multiple
              :objects="screens_list"
            ></auto-list>
          </div>

          <div class="d-flex gap-3 mt-7">
            <v-btn
              variant="tonal"
              class="flex-grow-1 action-btn-premium"
              @click="assignDialog.show = false"
              >{{ $t("syncCancel") }}</v-btn
            >
            <v-btn
              variant="tonal"
              color="primary"
              class="flex-grow-1 action-btn-premium"
              :loading="assignDialog?.loading"
              @click="confirmAssignment"
            >
              <v-icon icon="mdi-check" start></v-icon>
              {{ $t("syncConfirm") }}
            </v-btn>
          </div>
        </v-container>
      </template>
    </custom-dialog>

    <!-- Create Group Dialog -->
    <custom-dialog
      v-model="showAddGroup"
      width="450"
      height="auto"
      :title="$t('createPipeline')"
    >
      <template v-slot>
        <!-- <div class="dialog-header-icon mb-5">
        <v-icon icon="mdi-plus" size="24" color="white"></v-icon>
      </div> -->
        <v-container class="pa-8 py-5">
          <!-- <h2 class="text-h5 font-weight-black mb-2">Create Pipeline</h2> -->
          <!-- <p class="text-body-2 opacity-50 mb-3">
            {{ $t("designNewWorkflow") }}
          </p> -->

          <v-form ref="group_form">
            <fields :data="group_data" url="screen-sync" :attr="{}"></fields>
          </v-form>

          <div class="d-flex gap-3 mt-7">
            <v-btn
              variant="tonal"
              class="flex-grow-1 action-btn-premium"
              @click="showAddGroup = false"
              >{{ $t("syncCancel") }}</v-btn
            >
            <v-btn
              v-if="!group_data?.id"
              variant="tonal"
              color="primary"
              class="flex-grow-1 action-btn-premium"
              :loading="loading?.group_btn"
              @click="createGroup"
            >
              <v-icon icon="mdi-check" start></v-icon>
              {{ $t("createPipeline") }}
            </v-btn>
            <v-btn
              v-else
              variant="tonal"
              color="success"
              class="flex-grow-1 action-btn-premium"
              :loading="loading?.group_btn"
              @click="editGroup"
            >
              <v-icon icon="mdi-pencil" start></v-icon>
              {{ $t("edit_group") }}
            </v-btn>
          </div>
          <!-- <v-text-field
            v-model="newGroupName"
            label="Pipeline Name"
            variant="outlined"
            color="primary"
            class="premium-input mb-6"
            placeholder="e.g. Main Sync Flow"
            autofocus
            @keyup.enter="createGroup"
          ></v-text-field> -->
          <!-- <v-btn
            block
            height="48"
            class="action-btn-premium group-btn-primary"
            @click="createGroup"
          >
            <v-icon icon="mdi-check" start></v-icon>
            {{ $t("createPipeline") }}
          </v-btn> -->
        </v-container>
      </template>
    </custom-dialog>

    <!-- Premium Confirmation Dialog -->
    <v-dialog v-model="confirmDialog.show" max-width="400">
      <v-card class="premium-pulse-dialog pa-8 text-center">
        <div class="dialog-header-icon mb-5" :class="confirmDialog.type || 'error'">
          <v-icon
            color="white"
            size="28"
            :icon="
              confirmDialog.type === 'primary' || confirmDialog.type === 'info'
                ? 'mdi-information-outline'
                : 'mdi-alert-outline'
            "
          ></v-icon>
        </div>
        <h2 class="text-h5 font-weight-black mb-2">
          {{ confirmDialog.title }}
        </h2>
        <p class="text-body-2 opacity-50 mb-8">{{ confirmDialog.message }}</p>

        <div class="d-flex gap-3">
          <v-btn
            variant="tonal"
            class="flex-grow-1 action-btn-premium"
            @click="confirmDialog.show = false"
          >
            {{ $t("syncCancel") }}
          </v-btn>
          <v-btn
            variant="tonal"
            class="flex-grow-1 action-btn-premium"
            :color="confirmDialog.type || 'error'"
            :loading="confirmDialog?.loading"
            @click="confirmDialog.onConfirm()"
          >
            {{ $t("syncConfirm") }}
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </div>

  <!-- Sequence Error Dialog -->
  <v-dialog v-model="errorDialog.show" max-width="480" persistent>
    <div class="premium-pulse-dialog pa-8 text-center">
      <div class="dialog-header-icon error mb-5">
        <v-icon color="white" size="28" icon="mdi-alert-circle-outline"></v-icon>
      </div>
      <h2 class="text-h5 font-weight-black mb-2">
        {{ $t("errorDialog.title") }}
      </h2>
      <p class="text-body-2 opacity-50 mb-4">
        {{ $t("errorDialog.subtitle") }}
      </p>

      <div class="error-detail-box pa-4 mb-6">
        <div class="d-flex align-center gap-2 mb-2">
          <v-icon icon="mdi-monitor" size="16" color="error"></v-icon>
          <span class="text-body-2 font-weight-bold">{{ errorDialog.screenName }}</span>
        </div>
        <div class="text-body-2 opacity-60">
          {{ errorDialog.errorMessage }}
        </div>
        <div class="text-caption opacity-40 mt-2">
          {{
            $t("errorDialog.progress", {
              current: errorDialog.currentIndex,
              total: errorDialog.totalCount,
            })
          }}
        </div>
      </div>

      <div class="d-flex gap-3">
        <v-btn
          variant="tonal"
          color="error"
          class="flex-grow-1 action-btn-premium"
          @click="resolveErrorDialog(false)"
        >
          <v-icon icon="mdi-stop-circle-outline" start></v-icon>
          {{ $t("errorDialog.stop") }}
        </v-btn>
        <v-btn
          variant="tonal"
          color="primary"
          class="flex-grow-1 action-btn-premium"
          @click="resolveErrorDialog(true)"
        >
          <v-icon icon="mdi-play-circle-outline" start></v-icon>
          {{ $t("errorDialog.continue") }}
        </v-btn>
      </div>
    </div>
  </v-dialog>
  <!-- Sequence Error Dialog -->
  <v-dialog v-model="dialog_setting_edit" max-width="900">
    <v-card>
      <v-card-title class="text-h5 bg-primary text-white pa-4">
        {{ $t("setting_edit") }}
      </v-card-title>

      <v-card-text class="pa-4">
        <json-field
          v-model="single_group.settings"
          :label="$t('setting_data')"
          :indentation="3"
          auto-grow
          variant="outlined"
          rows="10"
          :rules="[jsonRule]"
          hide-details="auto"
          class="font-monospace"
        >
        </json-field>
      </v-card-text>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          color="grey-darken-1"
          variant="text"
          @click="dialog_setting_edit = false"
          >{{ $t("cancel") }}</v-btn
        >
        <v-btn
          color="success"
          variant="text"
          :disabled="!isValidJson"
          @click="saveSettingEdit"
          :loading="loading_save"
          >{{ $t("save") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- تاكيد الحذف الشاشة -->
  <!-- <confirm-deletion
    v-model="dialog_delete_group"
    :url="url_groups"
    :delete-item="group_data?.fk_group"
    :delRefresh="true"
    :getData="getGroup"
  /> -->
</template>

<script>
import draggable from "vuedraggable";

export default {
  components: {
    draggable,
  },
  data() {
    return {
      loading: {},
      loading_save: false,
      group_data: {},
      errorDialog: {},
      single_group: {},
      dialog_setting_edit: false,

      items: [],
      screens_list: [],
      sync_groups: [],

      url: "sync/screens/",
      url_groups: "sync/groups/",
      searchInput: "",
      appliedSearch: "",

      dialog_delete_group: false,
      stop_group_sequence: false,

      activityDrawer: false,
      globalSearch: "",
      isSyncingNew: false,
      assignDialog: {
        show: false,
        mode: "screen",
        screen: null,
        group: null,
        selectedGroups: [],
        selectedScreens: [],
      },
      showAddGroup: false,
      openPanels: [],
      compactGroups: new Set(),
      confirmDialog: {
        show: false,
        title: "",
        message: "",
        onConfirm: () => {},
      },
      statusScreen: {
        1: { color: "", icon: "mdi-sync-off" },
        2: { color: "teal", icon: "mdi-sync" },
        3: { color: "secondary", icon: "mdi-sync-alert" },
        4: { color: "error", icon: "mdi-alert-circle-outline" },
      },
      newGroupName: "",
    };
  },
  created() {
    this.getGroup();
  },
  computed: {
    isValidJson() {
      try {
        JSON.parse(this.single_group?.settings);
        return true;
      } catch (e) {
        return false;
      }
    },
    filteredGroups() {
      let groups = this.sync_groups;
      const q = (this.appliedSearch || "")?.toLowerCase();

      if (q) {
        groups = groups.filter(
          (g) =>
            g.name_ar?.toLowerCase()?.includes(q) ||
            g.screens.some((s) => s?.screen?.toLowerCase()?.includes(q))
        );
      }
      return groups;
    },
    // stats() {
    //   return getters.statistics.value;
    // },
    metricCards() {
      return [
        {
          key: "syncedScreens",
          label: this.$t("syncedScreens"),
          value: this.getMaterixData()?.synced,
          icon: "mdi-sync",
          color: "teal",
          colorClass: "teal",
        },
        {
          key: "needUpdateScreens",
          label: this.$t("needUpdateScreens"),
          value: this.getMaterixData()?.update,
          icon: "mdi-timer-sand",
          color: "amber",
          colorClass: "amber",
        },

        {
          key: "notSyncedScreens",
          label: this.$t("notSyncedScreens"),
          value: this.getMaterixData()?.unsynced,
          icon: "mdi-alert-octagon-outline",
          color: "slate",
          colorClass: "slate",
        },
        {
          key: "totalScreens",
          label: this.$t("totalScreens"),
          value: this.screens_list?.length,
          icon: "mdi-monitor-dashboard",
          color: "indigo",
          colorClass: "indigo",
        },
      ];
    },
  },
  watch: {
    searchInput(newVal) {
      if (!newVal) {
        this.appliedSearch = "";
      }
    },
  },
  methods: {
    jsonRule(value) {
      if (!value) return this.$t("input_required");
      try {
        JSON.parse(value);
        return true;
      } catch (e) {
        return this.$t("this_json_is_not_true");
      }
    },
    async getGroup() {
      try {
        this.loading.groups = true;
        const response = await this.$axios("sync/groups/all/");
        this.sync_groups = response.data?.data?.sort((a, b) => a.id - b.id);
        await this.getData();
      } catch (error) {
        console.log(error);
      } finally {
        this.loading.groups = false;
      }
    },

    async getData(fk_group) {
      try {
        if (!this.loading?.groups) {
          this.loading[`screens_${fk_group}`] = true;
        }
        const response = await this.$axios(this.url + "all/");
        this.items = response.data?.data;
        await this.filter_items(this.items);

        this.screens_list = response.data?.data
          ?.filter((sc) => sc?.screen)
          ?.map((s) => ({ ...s, name: s?.screen }));
      } catch (error) {
        console.log(error);
      } finally {
        this.loading[`screens_${fk_group}`] = false;
      }
    },
    // formate and joins the screens to its own group
    async filter_items(items) {
      let result = this.sync_groups?.reduce((acc, obj) => {
        acc[obj?.name_ar] = [];
        return acc;
      }, {});

      items.forEach((screen) => {
        screen.current_groups.forEach((group) => {
          const data = {
            id: screen.id,
            fk_screen: screen.fk_screen,
            status: screen.status,
            last_synced_at: screen.last_synced_at,

            main_model: screen.main_model,
            remote_prefix_url: screen.remote_prefix_url,
            screen: screen.screen,
            status_name: screen.status_name,
            screen_icon: screen.screen_icon,

            group_id: group.id,
            groups: [group.fk_sync_group],
            fk_sync_group: group.fk_sync_group,
            group_name: group.group_name,
            order: group.order,
            settings: group.settings,
            screens: [],

            settings_edit_loading: false,
          };

          if (!Array?.isArray(result[group.group_name])) {
            result[group.group_name] = [];
          }

          result[group.group_name].push(data);
        });
      });
      for (const key in result) {
        if (
          Object.prototype.hasOwnProperty.call(result, key) &&
          Array.isArray(result[key])
        ) {
          if (this.sync_groups.find((g) => g?.name_ar == key)) {
            this.sync_groups.find((g) => g?.name_ar == key).screens = result[key].sort(
              (a, b) => a.order - b.order
            );
          }
        }
      }
    },

    async syncScreen(screen, method, group) {
      try {
        if (!screen[method]) {
          screen[method] = {};
        }
        screen[method].loading = true;
        const res = await this.$axios(`sync/screens/${screen.id}/${method}-by-id/`, {
          params: {
            group: screen.fk_sync_group,
          },
        });
        const res_data = res?.data?.data;
        if (method == "push") {
          this.updateScreensStatus(res_data?.screen_id, res_data);
        }
        this.$snack("success", {
          message: `${screen?.screen} ( ${res_data?.sync_status_display} )`,
        });
        // await this.getData();
      } catch (error) {
        const err = error?.response?.data;
        if (method == "push" && !err?.success && error?.response) {
          screen.status_name = "فشلت المزامنه";
          screen.status = 4;
          console.log(err);
          screen.sync_error = err?.message;
          return false;
        }
        console.log(error);
        return false;
      } finally {
        screen[method].loading = false;
      }
    },
    updateScreensStatus(fk_screen, new_data) {
      for (const group of this.sync_groups) {
        const screens = group?.screens;

        if (!screens) continue;
        let screen = screens?.find((s) => s?.id == fk_screen);
        if (screen) {
          screen.status = new_data?.sync_status;
          screen.status_name = new_data?.sync_status_display;
        }
      }
    },

    async runGroupSequence(group, method) {
      try {
        this.confirmDialog.show = false;
        this.loading[`${method}_${group?.id}`] = true;
        for (const screen of group.screens?.filter((s) =>
          method == "pull" ? s?.settings?.can_pull : s?.status != 2
        )) {
          const res = await this.syncScreen(screen, method);
          if (res == false || this.stop_group_sequence) {
            this.stop_group_sequence = false;
            break;
          }
        }
      } catch (error) {
        console.log(error);
      } finally {
        this.loading[`${method}_${group?.id}`] = false;
      }
    },

    confirmAndRunGroupSequence(group, type = "push") {
      console.log(group.screens?.filter((s) => s?.settings?.can_pull)?.length);
      const title =
        type === "push"
          ? this.$t("uploadAllConfirmTitle")
          : this.$t("downloadAllConfirmTitle");
      const message =
        type === "push"
          ? this.$t("uploadAllConfirmMsg", {
              count: group.screens?.filter((s) => s?.status != 2)?.length,
            })
          : this.$t("downloadAllConfirmMsg", {
              count: group.screens?.filter((s) => s?.settings?.can_pull)?.length,
            });

      this.openConfirm(
        title,
        message,
        () => {
          this.runGroupSequence(group, type);
        },
        "primary"
      );
    },

    async syncAllNewScreens() {
      try {
        this.loading.sync_screen = true;
        await this.$axios(this.url + "regester-screen/");
        await this.getGroup();
      } catch (error) {
        console.log(error);
      } finally {
        this.loading.sync_screen = false;
        this.loading.groups = false;
      }
    },

    async onDragChange(evt, group) {
      try {
        const elm = evt?.moved;
        const res = await this.$axios.put(
          `sync/screens/${elm?.element?.id}/assign-order/`,
          {
            order: elm?.newIndex + 1,
            group: group?.id,
          }
        );
      } catch (error) {
        // await this.getData();
        console.log(error);
      }
      // screens.forEach((screen, index) => {
      //   screen.order = index + 1;
      // });
    },
    async OpenDialogSettingEdit(id, screen, method) {
      if (!screen[method]) {
        screen[method] = {};
      }
      screen[method].loading = true;
      if (id) {
        const res = await this.$axios(`sync/screen-group/${id}`);
        if (res) {
          this.single_group = {
            ...res.data.data,
            settings: JSON.stringify(res.data.data.settings, null, 2),
          };

          this.dialog_setting_edit = true;
        }
      } else {
        this.alert("errorData", { message: "error in response" + res });
      }
      screen[method].loading = false;
    },

    async saveSettingEdit() {
      if (!this.single_group?.id) return;
      try {
        this.loading_save = true;
        const res = await this.$axios.put(`sync/screen-group/${this.single_group.id}/`, {
          ...this.single_group,
          settings: JSON.parse(this.single_group?.settings),
        });
        if (
          res.success === true ||
          res?.data?.success == true ||
          res?.data?.data?.success == true
        ) {
          this.$snack("success", { message: this.$t("saved_successfully") });
          this.dialog_setting_edit = false;
        } else {
          this.$alert("errorData", { message: "error in response" + res });
        }
      } catch (e) {
        this.$alert("errorData", { message: e });
      } finally {
        this.loading_save = false;
      }
    },

    getStatusColor(status) {
      if (status == 3) return "warning";
      if (status == 2) return "success";
      if (status == 4) return "error";
      return "grey";
    },
    getStatusIcon(status) {
      if (status == 3) return "mdi-timer-sand";
      if (status == 2) return "mdi-check-circle";
      if (status == 4) return "mdi-alert-circle";
      return "mdi-clock-outline";
    },

    openConfirm(title, message, onConfirm, type = "error") {
      this.confirmDialog = {
        show: true,
        title,
        message,
        onConfirm,
        type,
      };
    },
    isCompact(groupId) {
      return this.compactGroups.has(groupId);
    },
    toggleCompact(groupId) {
      if (this.compactGroups.has(groupId)) this.compactGroups.delete(groupId);
      else this.compactGroups.add(groupId);
    },

    getHealthColor(rate) {
      if (rate > 90) return "#10b981";
      if (rate > 70) return "#f59e0b";
      return "#ef4444";
    },

    // getGroupFailedCount(group) {
    //   return group?.screens?.filter((s) => s.status === "failed").length;
    // },

    showBulkScreenDialog(group) {
      this.assignDialog = {
        show: true,
        mode: "group",
        group,
        selectedScreens: [],
        selectedGroups: [group.id],
      };
    },
    async confirmAssignment() {
      try {
        this.assignDialog.loading = true;
        await this.$axios.post("sync/screens/assign-screens-to-group/", {
          screens: this.assignDialog?.selectedScreens,
          group: this.assignDialog?.group?.id,
        });
        this.getData(this.assignDialog?.group?.id);
        this.assignDialog.show = false;
      } catch (error) {
        console.log(error);
        this.assignDialog.loading = false;
      }
    },
    async createGroup() {
      try {
        if (await this.$validate(this.$refs["group_form"])) {
          this.loading.group_btn = true;
          await this.$axios?.post(this.url_groups, this.group_data);
          this.$snack("added");
          this.getGroup();
          this.showAddGroup = false;
        }
      } catch (error) {
        console.log(error);
      } finally {
        this.loading.group_btn = false;
      }
    },
    async editGroup() {
      try {
        if (await this.$validate(this.$refs["group_form"])) {
          this.loading.group_btn = true;
          await this.$axios?.put(
            this.url_groups + this.group_data?.id + "/",
            this.group_data
          );
          this.$snack("update");
          this.getGroup();
          this.showAddGroup = false;
        }
      } catch (error) {
        console.log(error);
      } finally {
        this.loading.group_btn = false;
      }
    },

    // openGroupDialog() {
    //   this.openConfirm(
    //     this.$t("deletePipelineConfirm"),
    //     this.$t("deletePipelineMsg", { name: group?.name || "" }),
    //     () => this.confirmDeleteGroup(groupId)
    //   );
    // },
    openEditGroupDialog(group) {
      this.group_data = group;
      this.showAddGroup = true;
    },
    confirmDeleteGroup(group) {
      this.openConfirm(
        this.$t("removeGroupConfirm"),
        this.$t("removeGroupMsg", {
          pipeline: group?.name_ar,
        }),
        () => this.removeGroup(group?.id)
      );
    },
    async removeGroup(groupId) {
      try {
        this.confirmDialog.loading = true;
        await this.$axios.delete(`sync/screens/${groupId}/delete-group/`);
        this.$snack("success");
        await this.getGroup();
        this.confirmDialog.show = false;
      } catch (error) {
        console.log(error);
      } finally {
        this.confirmDialog.loading = false;
      }
    },

    openScreenDialog(screen, group) {
      this.openConfirm(
        this.$t("removeScreenConfirm"),
        this.$t("removeScreenMsg", {
          screen: screen?.screen,
          pipeline: group?.name_ar,
        }),
        () => this.removeScreenFromGroup(screen?.group_id)
      );
    },
    async removeScreenFromGroup(groupId) {
      try {
        this.confirmDialog.loading = true;
        const res = await this.$axios.delete(
          `sync/screens/${groupId}/disengagement-from-group/`
        );
        this.$snack("success", { message: res?.data?.message });
        await this.getData();
        this.confirmDialog.show = false;
      } catch (error) {
        console.log(error);
      } finally {
        this.confirmDialog.loading = false;
      }
    },

    getMaterixData() {
      if (this.sync_groups?.length) {
        const status_labels = {
          1: "unsynced",
          2: "synced",
          3: "update",
        };

        const seen = new Set();
        const counts = {
          unsynced: 0,
          synced: 0,
          update: 0,
        };

        for (const group of this.sync_groups) {
          const screens = group?.screens || [];

          for (const s of screens) {
            if (!s || s?.id == null || seen?.has(s?.id)) continue;

            seen?.add(s?.id);

            const status = s?.status;
            if (status == null) continue;
            counts[status_labels[status]] = (counts[status_labels[status]] || 0) + 1;
          }
        }

        return counts;
      }
    },

    async handleSearch() {
      this.loading.groups = true;
      this.appliedSearch = this.searchInput;

      this.loading.groups = false;
    },
    handleClearSearch() {
      this.searchInput = "";
      this.appliedSearch = "";
      this.loading.groups = false;
    },
    getLogIcon(type) {
      const icons = {
        success: "mdi-check-circle",
        error: "mdi-alert-circle",
        upload: "mdi-cloud-upload",
        download: "mdi-cloud-download",
        info: "mdi-information",
      };
      return icons[type] || "mdi-text-box-outline";
    },
    formatTime(ts) {
      if (!ts) return "";
      return new Date(ts).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    },

    isGrroupEmpty(group, method = false) {
      if (method) {
        return (
          group?.screens?.length === 0 ||
          !group?.screens?.find((s) =>
            method == "pull" ? s?.settings?.can_pull : [1, 3, 4]?.includes(s?.status)
          )
        );
      }
      return group?.screens?.length === 0;
    },
  },
};
</script>

<style scoped>
/* ═══════════════════════════════════════
   BASE LAYOUT
   ═══════════════════════════════════════ */

.main-pulse-layout {
  min-height: 100%;
  /* background: rgb(var(--v-theme-background)); */
  font-family: "Inter", sans-serif;
  overflow-x: hidden;
  /* color: rgb(var(--v-theme-on-background)); */
  transition: background 0.4s ease, color 0.4s ease;
}

.main-pulse-layout .text-h3,
.main-pulse-layout .text-h4,
.main-pulse-layout .text-h5,
.main-pulse-layout .text-h6,
.main-pulse-layout .text-subtitle-1,
.main-pulse-layout .text-body-2,
.main-pulse-layout .text-caption,
.main-pulse-layout .text-overline {
  /* color: rgb(var(--v-theme-on-background)); */
}

/* ═══════════════════════════════════════
   DECORATIVE ORBS
   ═══════════════════════════════════════ */

.glass-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(140px);
  z-index: 0;
  opacity: 0.07;
  pointer-events: none;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: #6366f1;
  top: -150px;
  right: -150px;
  animation: orb-float 20s ease-in-out infinite;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: #06b6d4;
  bottom: -100px;
  left: -100px;
  animation: orb-float 25s ease-in-out infinite reverse;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: #8b5cf6;
  top: 50%;
  right: 50%;
  transform: translate(-50%, -50%);
  animation: orb-float 30s ease-in-out infinite;
}

@keyframes orb-float {
  0%,
  100% {
    transform: translate(0, 0);
  }

  25% {
    transform: translate(30px, -20px);
  }

  50% {
    transform: translate(-20px, 30px);
  }

  75% {
    transform: translate(20px, 20px);
  }
}

/* ═══════════════════════════════════════
   PAGE HEADER & SEARCH
   ═══════════════════════════════════════ */

.page-title {
  letter-spacing: -0.5px;
}

.search-field :deep(.v-field) {
  border-radius: 14px !important;
  background: rgba(var(--v-theme-on-surface), 0.04) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08) !important;
  transition: all 0.2s ease;
}

.search-field :deep(.v-field:hover) {
  background: rgba(var(--v-theme-on-surface), 0.06) !important;
}

.search-field :deep(.v-field--focused) {
  background: rgba(var(--v-theme-on-surface), 0.02) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.1) !important;
}

/* ═══════════════════════════════════════
   ACTIVITY DRAWER
   ═══════════════════════════════════════ */

.activity-drawer {
  background: rgb(var(--v-theme-surface)) !important;
  border-right: 1px solid rgba(var(--v-theme-on-surface), 0.08) !important;
}

.drawer-icon-box {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-log-item {
  padding: 14px 16px;
  background: rgba(var(--v-theme-on-surface), 0.03);
  border-radius: 14px;
  border-right: 3px solid transparent;
  transition: all 0.2s ease;
  animation: slide-in-left 0.3s ease forwards;
  opacity: 0;
}

@keyframes slide-in-left {
  from {
    opacity: 0;
    transform: translateX(-12px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.activity-log-item:hover {
  background: rgba(var(--v-theme-on-surface), 0.05);
}

.activity-log-item.success {
  border-right-color: #10b981 !important;
}

.activity-log-item.error {
  border-right-color: #ef4444 !important;
}

.activity-log-item.upload {
  border-right-color: #8b5cf6 !important;
}

.activity-log-item.download {
  border-right-color: #3b82f6 !important;
}

.activity-log-item.info {
  border-right-color: #6366f1 !important;
}

.log-type-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(var(--v-theme-on-surface), 0.3);
}

.log-type-dot.success {
  background: #10b981;
}

.log-type-dot.error {
  background: #ef4444;
}

.log-type-dot.upload {
  background: #8b5cf6;
}

.log-type-dot.download {
  background: #3b82f6;
}

.log-type-dot.info {
  background: #6366f1;
}

/* ═══════════════════════════════════════
   HEALTH MATRIX (METRIC CARDS)
   ═══════════════════════════════════════ */

.health-matrix-node {
  position: relative;
  /* background: rgba(var(--v-theme-on-surface), 0.03); */
  background: #f8fafc1a;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 20px;
  padding: 24px;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fade-up 0.5s ease forwards;
  opacity: 0;
}
.metric-label {
  font-size: 0.8rem;
  font-weight: 900;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(16px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.health-matrix-node:hover {
  /* transform: translateY(-4px);
  border-color: rgba(var(--v-theme-on-surface), 0.12);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08); */
  transform: translateY(-4px);
  border-color: rgba(203, 213, 225, 0.6);
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.06), 0 12px 24px -8px rgba(0, 0, 0, 0.1);

  --card-accent: red !important;
}

.node-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: currentColor;
  opacity: 0.4;
}

.health-matrix-node.cyan {
  color: #06b6d4;
}

.health-matrix-node.indigo {
  color: #5a8dee;
}

.health-matrix-node.emerald {
  color: #10b981;
}

.health-matrix-node.rose {
  color: #ef4444;
}
.health-matrix-node.teal {
  color: #14b8a6;
}
.health-matrix-node.amber {
  color: #f59e0b;
}
.health-matrix-node.slate {
  color: #64748b;
}

.metric-label {
  font-size: 10px !important;
  letter-spacing: 1.5px !important;
}

.metric-value {
  font-family: "JetBrains Mono", monospace;
  font-size: 36px;
  font-weight: 800;
  line-height: 1;
  color: rgb(var(--v-theme-on-background));
}

.metric-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.health-matrix-node:hover .metric-icon-box {
  transform: scale(1.1);
}
.metric-icon-box.indigo {
  background: linear-gradient(135deg, #5a8dee 0%, #80a8f2 100%);
  box-shadow: 0 4px 14px rgba(99, 163, 241, 0.3);
}

.metric-icon-box.rose {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
}

.metric-icon-box.cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
  box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
}

.metric-icon-box.emerald {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
}
.metric-icon-box.teal {
  background: linear-gradient(135deg, #14b8a6 0%, #2dd4bf 100%);
  box-shadow: 0 4px 14px rgba(20, 184, 166, 0.3);
}
.metric-icon-box.amber {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);
}
.metric-icon-box.slate {
  background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
  box-shadow: 0 4px 14px rgba(100, 116, 139, 0.3);
}

.sync-pulse-btn {
  animation: gentle-pulse 2s infinite;
}

@keyframes gentle-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.3);
  }

  50% {
    box-shadow: 0 0 0 6px rgba(var(--v-theme-primary), 0);
  }
}

/* ═══════════════════════════════════════
   PIPELINE CARDS
   ═══════════════════════════════════════ */

.pipeline-card-glass {
  /* background: rgba(var(--v-theme-on-surface), 0.02); */
  background: #f8fafc04;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.07);
  border-radius: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.35s ease;
  animation: fade-up 0.5s ease forwards;
  opacity: 0;
}

.pipeline-card-glass:hover {
  background: rgba(var(--v-theme-on-surface), 0.01);
  border-color: rgba(var(--v-theme-on-surface), 0.12);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.06);
}

.pipeline-header {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.pipeline-badge {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #5a8dee 0%, #80a8f2 100%);
  box-shadow: 0 3px 10px rgba(99, 102, 241, 0.25);
  flex-shrink: 0;
  /* background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%); */
}

.failed-count-badge {
  color: #ef4444;
}

.header-action-btn {
  transition: opacity 0.2s ease;
}

.header-action-btn:hover {
  opacity: 0.9 !important;
}

.pipeline-body {
  transition: max-height 0.3s ease;
  flex-grow: 1;
}

.pipeline-body.is-scrollable {
  max-height: 390px;
  overflow-y: auto;
}

/* ═══════════════════════════════════════
   LOGIC NODE CARDS (SCREEN ITEMS)
   ═══════════════════════════════════════ */

.logic-node-card {
  background: rgba(var(--v-theme-on-surface), 0.03);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 14px;
  padding: 10px 12px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  transition: all 0.25s ease;
}

.logic-node-card:hover {
  background: rgba(var(--v-theme-on-surface), 0.06);
  border-color: rgba(var(--v-theme-on-surface), 0.12);
}

.logic-node-card.is-compact {
  padding: 6px 10px;
  margin-bottom: 4px;
  border-radius: 10px;
}

.logic-node-card.is-compact .node-health-progress {
  display: none;
}

.logic-node-card.is-compact .type-chip-enhanced {
  display: none;
}

.logic-node-card.is-active {
  border-color: rgba(99, 102, 241, 0.4);
  background: rgba(99, 102, 241, 0.05);
  box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.1), 0 4px 16px rgba(99, 102, 241, 0.08);
  animation: active-pulse 2s infinite;
}

@keyframes active-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.1), 0 4px 16px rgba(99, 102, 241, 0.08);
  }

  50% {
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2), 0 4px 20px rgba(99, 102, 241, 0.12);
  }
}

.logic-node-card.is-success {
  border-right: 3px solid #10b981;
}

.logic-node-card.is-failed {
  border-right: 3px solid #ef4444;
  background: rgba(239, 68, 68, 0.03);
}
.logic-node-card.is-new-updates {
  border-right: 3px solid #efcd44;
  background: rgba(239, 191, 68, 0.03);
}

.node-drag-handle {
  cursor: grab;
  padding: 4px;
  margin-left: 4px;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.node-drag-handle:hover {
  background: rgba(var(--v-theme-on-surface), 0.06);
}

.node-drag-handle:active {
  cursor: grabbing;
}

.node-id-tag {
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  font-weight: 800;
  color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.1);
  width: 22px;
  height: 22px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.node-health-progress {
  opacity: 0.7;
  border-radius: 4px !important;
}

/* Type Chips */
.type-chip-enhanced {
  font-size: 9px !important;
  height: 20px !important;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.5px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06) !important;
  padding: 0 8px !important;
  /* background: rgba(var(--v-theme-on-surface), 0.06) !important; */
  /* color: rgba(var(--v-theme-on-surface), 0.55) !important; */
}

.type-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  margin-right: 4px;
  flex-shrink: 0;
}

.type-dot.upload {
  background: #8b5cf6;
}

.type-dot.request {
  background: #3b82f6;
}

/* Node Actions */
.node-action-btn {
  opacity: 0.5;
  transition: all 0.2s ease !important;
  width: 28px !important;
  height: 28px !important;
}

.node-action-btn:hover {
  opacity: 1 !important;
  background: rgba(var(--v-theme-on-surface), 0.06) !important;
}

.node-status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.spin-animation {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* ═══════════════════════════════════════
   SKELETON LOADING
   ═══════════════════════════════════════ */

.skeleton-pipeline-card {
  pointer-events: none;
}

.skeleton-bone {
  background: rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.skeleton-bone::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(var(--v-theme-on-surface), 0.06) 50%,
    transparent 100%
  );
  animation: skeleton-shimmer 1.6s ease-in-out infinite;
}

@keyframes skeleton-shimmer {
  0% {
    left: -100%;
  }

  100% {
    left: 100%;
  }
}

/* ═══════════════════════════════════════
   PIPELINE FOOTER
   ═══════════════════════════════════════ */

.pipeline-footer {
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

/* ═══════════════════════════════════════
   EMPTY STATES
   ═══════════════════════════════════════ */

.empty-pipeline-state {
  padding: 48px 20px;
  text-align: center;
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 16px;
  transition: border-color 0.3s ease;
}

.empty-pipeline-state:hover {
  border-color: rgba(var(--v-theme-on-surface), 0.15);
}

.empty-icon-container {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: rgba(var(--v-theme-on-surface), 0.04);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.no-pipelines-empty {
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 28px;
  position: relative;
  overflow: hidden;
}

.empty-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.empty-icon-float {
  animation: float-gentle 3s ease-in-out infinite;
}

@keyframes float-gentle {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-8px);
  }
}

/* ═══════════════════════════════════════
   BUTTONS & INPUTS
   ═══════════════════════════════════════ */

.action-btn-premium {
  text-transform: none;
  font-weight: 700;
  letter-spacing: 0.1px;
  border-radius: 12px;
  transition: all 0.25s ease;
}

.action-btn-premium:hover {
  transform: translateY(-1px);
}

.group-btn-primary {
  /* background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
  color: white !important; */
  box-shadow: 0 4px 14px rgba(99, 163, 241, 0.3);
}

.group-btn-primary:hover {
  box-shadow: 0 6px 20px rgba(99, 163, 241, 0.3) !important;
}

.premium-input :deep(.v-field) {
  border-radius: 14px !important;
  background: rgba(var(--v-theme-on-surface), 0.03) !important;
}

.premium-input :deep(.v-field:hover) {
  background: rgba(var(--v-theme-on-surface), 0.05) !important;
}

/* ═══════════════════════════════════════
   SECTION DECOR
   ═══════════════════════════════════════ */

.section-accent {
  width: 4px;
  height: 40px;
  background: linear-gradient(to bottom, #5a8dee, rgba(99, 102, 241, 0.2));
  border-radius: 4px;
  /* background: linear-gradient(to bottom, #6366f1, rgba(99, 102, 241, 0.2)); */
}

.border-t-glass {
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.border-b-glass {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

/* ═══════════════════════════════════════
   DIALOGS
   ═══════════════════════════════════════ */

.premium-pulse-dialog {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 24px !important;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
}

.dialog-header-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(99, 163, 241, 0.3);
}

.dialog-header-icon.error {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
}
.dialog-header-icon.primary {
  background: linear-gradient(135deg, #5a8dee 0%, #80a8f2 100%);
  box-shadow: 0 4px 14px rgba(99, 163, 241, 0.3);
}

.glass-list-premium {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* ═══════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════ */

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.12);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.2);
}

.gap-1 {
  gap: 0.25rem;
}
.gap-2 {
  gap: 0.5rem;
}
.gap-3 {
  gap: 0.75rem;
}
</style>
