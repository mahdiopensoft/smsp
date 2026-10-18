<template>
  <v-form ref="form">
    <!-- Top form fields panel -->
    <v-card
      v-if="withFields"
      elevation="0"
      rounded="0"
      class="hide-item border-b"
    >
      <!-- Header row: title on left, actions on right -->
      <div class="d-flex align-center justify-space-between px-4 py-2 border-b">
        <div class="d-flex align-center gap-2">
          <v-icon color="primary" size="18">mdi-table-plus</v-icon>
          <span
            class="text-body-2 font-weight-bold"
            style="color: rgb(var(--v-theme-on-surface))"
          >
            {{
              index_item >= 0
                ? $i18n.locale == "ar"
                  ? "تعديل السجل"
                  : "Edit Record"
                : $i18n.locale == "ar"
                ? "إضافة سجل جديد"
                : "Add New Record"
            }}
          </span>
        </div>
      </div>
      <v-row>
        <fields :data="data" :fields="filter_fields" />
        <slot name="fields" :item="data" />

        <v-col class="pt-2">
          <custom-btn
            :type="index_item >= 0 ? 'update' : 'add'"
            @click="index_item >= 0 ? update() : add()"
          />
          <custom-btn
            v-if="index_item >= 0"
            type="cancel"
            @click="(index_item = undefined), (data = {})"
            is-icon
            class="ms-2"
          />
        </v-col>
      </v-row>
    </v-card>

    <!-- Top slot (when no withFields) -->
    <div
      v-if="!withFields"
      class="d-flex align-center px-4 py-3 custom-data-table-toolbar bg-surface border-b gap-2"
    >
      <div class="d-flex align-center gap-2">
        <custom-btn
          :type="index_item >= 0 ? 'update' : 'add'"
          @click="index_item >= 0 ? update() : add()"
        />
        <custom-btn
          v-if="index_item >= 0"
          type="cancel"
          @click="(index_item = undefined), (value = {})"
          is-icon
          class="ms-2"
        />
      </div>
    </div>
  </v-form>

  <VDataTableVirtual
    :headers="filter_headers"
    :items="items"
    :no-data-text="$t('not-found')"
    density="compact"
    class="custom-data-table border-sm"
  >
    <template #no-data>
      <NotFound />
    </template>

    <template
      v-for="header in filter_headers"
      :key="header.key"
      v-slot:[`item.${header.key}`]="{ item, index }"
    >
      <slot
        v-if="$slots[`item.${header.key}`]"
        :name="`item.${header.key}`"
        :item="item"
      ></slot>
      <template v-else>
        <td v-if="'nameList' in header">
          {{ getLabel(header.nameList, item[header.key]) }}
        </td>
        <template v-else-if="header.key === 'actions'">
          <span v-if="actions" class="d-flex align-center gap-1">
            <!-- Edit/Update button -->
            <custom-btn
              type="update"
              is-icon
              variant="tonal"
              class="row-action-btn"
              :click="() => edit(item, index)"
            />
            <!-- Delete/Remove button -->
            <custom-btn
              type="del"
              is-icon
              variant="tonal"
              class="row-action-btn"
              :click="() => remove(index)"
            />
          </span>
        </template>
        <td v-else>{{ item[header.key] }}</td>
      </template>
    </template>
  </VDataTableVirtual>
</template>



<script>
import NotFound from "../../other/NotFound.vue";
import { state } from "@/store/state";

export default {
  components: {
    NotFound,
  },
  props: {
    headers: {
      type: Array,
      default: [],
    },
    items: {
      type: Array,
      default: [],
    },
    actions: {
      type: Boolean,
      default() {
        return true;
      },
    },
    fields: {
      type: Array,
      default() {
        return [];
      },
    },
    withFields: {
      type: Boolean,
      default() {
        return true;
      },
    },
    modelValue: {
      type: Object,
    },
  },
  data() {
    return {
      data: {},
      index_item: undefined,
    };
  },

  methods: {
    getLabel(nameList, item) {
 
      const list = state?.autolist_data[nameList] || undefined;
      if (list) {
        if(list.list){
          

          const ele = list.list.find((e) => e.id == item);

        return ele?.name || ele?.name_ar || item;
        
        }}
        
        return item;
      
    },
    async add() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        if (this.withFields) {
          this.items.push({ ...this.data });
          this.data = {};
        } else {
          this.items.push({ ...this.value });
          this.value = {};
        }
      }
    },
    remove(index) {
      this.items.splice(index, 1);
    },
    edit(item, index) {
      if (this.withFields) this.data = { ...item };
      else this.value = { ...item };

      this.index_item = index;
    },
    async update() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        if (this.withFields) {
          this.items[this.index_item] = { ...this.data };
          this.index_item = undefined;
          this.data = {};
        } else {
          this.items[this.index_item] = { ...this.value };
          this.index_item = undefined;
          this.value = {};
        }
      }
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },

    filter_fields() {
      var list = [];
      this.headers.map((e) => {
        if (e.field) list.push(e.field);
      });
      return list;
    },
    filter_headers() {
      if (this.actions)
        return [
          ...this.headers,
          { title: this.$t("actions"), key: "actions", sortable: false },
        ];
      else return this.headers;
    },
  },
};
</script>
