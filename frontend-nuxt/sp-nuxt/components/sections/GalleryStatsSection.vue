<script setup>
import { onBeforeUnmount, onMounted, ref, computed, watch } from "vue";
import basePlanImage from "~/assets/resort/base-plan.webp";

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false,
  },
});

const isVisible = ref(false);
const sectionRef = ref(null);
const editablePlanTitle = ref("План базы отдыха");
const editablePlanDescription1 = ref("Откройте для себя место, где каждый уголок создан для незабываемых моментов.");
const editablePlanDescription2 = ref("Уютные домики среди вековых сосен, живописная набережная реки Камы, зоны для активного отдыха и тихие уголки для уединения — всё расположено так, чтобы ваш отдых стал по-настоящему особенным.");
const editableStats = ref([]);
const statsSavePending = ref(false);
const statsSaveError = ref("");
const statsSaveSuccess = ref("");

const {statistics: stats, refresh: refreshStatistics} = useStatistics({ordering: 'order'});
const { galleryImages, refresh: refreshGalleryMain } = useGallery({ position: 'main', ordering: 'order' });
const { get: getAdminContent, patch: patchAdminContent, post: postAdminContent, postForm: postAdminContentForm } = useAdminContentApi();
const editableGalleryImages = ref([]);
const gallerySourceImages = ref([]);
const localObjectUrls = ref([]);
const gallerySavePending = ref(false);
const gallerySaveError = ref("");
const gallerySaveSuccess = ref("");

const toNumberOrZero = (value) => {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : 0;
};

const createEditableGalleryItem = (item) => ({
  id: item?.id,
  sourceImageId: item?.id,
  sourceType: "db",
  order: toNumberOrZero(item?.order),
  position: item?.position || "main",
  column: item?.column || "left",
  alt_text: item?.alt_text || "",
  image_webp_url: item?.image_webp_url || item?.image_url || "",
  image_placeholder_url: item?.image_placeholder_url || null,
  image_url: item?.image_url || item?.image_webp_url || "",
  localPreviewUrl: null,
  localFile: null,
  localFileName: "",
});

const releaseObjectUrl = (url) => {
  if (!url || !import.meta.client) return;
  URL.revokeObjectURL(url);
  localObjectUrls.value = localObjectUrls.value.filter((item) => item !== url);
};

watch(
  stats,
  (value) => {
    editableStats.value = (value || []).map((item) => ({
      id: item?.id,
      number: item?.number || "",
      label: item?.label || "",
      description: item?.description || "",
    }));
  },
  { immediate: true }
);

watch(
  galleryImages,
  (value) => {
    editableGalleryImages.value = (value || [])
      .filter((item) => item?.position === "main" && item?.is_active)
      .map(createEditableGalleryItem);
  },
  { immediate: true }
);

const displayedStats = computed(() => {
  if (!props.editMode) return stats.value;
  return editableStats.value;
});

const activeGallerySource = computed(() => {
  const byId = new Map();
  (gallerySourceImages.value || []).forEach((item) => {
    if (byId.has(item.id)) return;
    byId.set(item.id, item);
  });
  return Array.from(byId.values());
});

const refreshGallerySource = async () => {
  if (!props.editMode) return;
  try {
    const data = await getAdminContent("/auth/edit/gallery/all/");
    gallerySourceImages.value = Array.isArray(data) ? data : (data?.results || []);
  } catch (_error) {
    gallerySourceImages.value = [];
  }
};

const editableByColumn = computed(() => {
  return editableGalleryImages.value.reduce((acc, image) => {
    const key = image?.column || "left";
    if (!acc[key]) acc[key] = [];
    acc[key].push(image);
    return acc;
  }, { left: [], center: [], right: [] });
});

const sortByOrder = (items) => {
  return [...(items || [])].sort((a, b) => {
    const orderDiff = toNumberOrZero(a?.order) - toNumberOrZero(b?.order);
    if (orderDiff !== 0) return orderDiff;
    return toNumberOrZero(a?.id) - toNumberOrZero(b?.id);
  });
};

const hasStatsChanges = computed(() => {
  const sourceById = new Map((stats.value || []).map((item) => [item.id, item]));
  return editableStats.value.some((item) => {
    const source = sourceById.get(item.id);
    if (!source) return false;
    return (
      item.number !== (source.number || "") ||
      item.label !== (source.label || "") ||
      (item.description || "") !== (source.description || "")
    );
  });
});

const saveStatistics = async () => {
  if (statsSavePending.value || !hasStatsChanges.value) return;

  statsSavePending.value = true;
  statsSaveError.value = "";
  statsSaveSuccess.value = "";

  try {
    const sourceById = new Map((stats.value || []).map((item) => [item.id, item]));
    const changed = editableStats.value.filter((item) => {
      const source = sourceById.get(item.id);
      if (!source) return false;
      return (
        item.number !== (source.number || "") ||
        item.label !== (source.label || "") ||
        (item.description || "") !== (source.description || "")
      );
    });

    for (const item of changed) {
      await patchAdminContent(`/auth/edit/statistics/${item.id}/`, {
        number: item.number,
        label: item.label,
        description: item.description,
      });
    }

    await refreshStatistics();
    statsSaveSuccess.value = "Статистика сохранена";
  } catch (error) {
    statsSaveError.value = error?.data?.detail || "Не удалось сохранить статистику";
  } finally {
    statsSavePending.value = false;
  }
};

// Распределяем изображения по колонкам на основе поля column
const leftColumn = computed(() => {
  if (props.editMode) return sortByOrder(editableByColumn.value.left);
  return galleryImages.value
    .filter(img => img.position === 'main' && img.column === 'left' && img.is_active)
    .sort((a, b) => a.order - b.order);
});

const centerColumn = computed(() => {
  if (props.editMode) return sortByOrder(editableByColumn.value.center);
  return galleryImages.value
    .filter(img => img.position === 'main' && img.column === 'center' && img.is_active)
    .sort((a, b) => a.order - b.order);
});

const rightColumn = computed(() => {
  if (props.editMode) return sortByOrder(editableByColumn.value.right);
  return galleryImages.value
    .filter(img => img.position === 'main' && img.column === 'right' && img.is_active)
    .sort((a, b) => a.order - b.order);
});

const getImageDisplaySrc = (image) => {
  return image?.localPreviewUrl || image?.image_webp_url || image?.image_url || "";
};

const getImageDisplayPlaceholder = (image) => {
  if (image?.localPreviewUrl) return null;
  return image?.image_placeholder_url || null;
};

const isLocalPreview = (image) => {
  return Boolean(image?.localPreviewUrl);
};

const getSourcePreviewSrc = (source) => {
  return source?.image_webp_url || source?.image_url || "";
};

const isSourceSelected = (image, source) => {
  return toNumberOrZero(image?.sourceImageId) === toNumberOrZero(source?.id);
};

const updateImageOrder = (image, nextOrder) => {
  image.order = toNumberOrZero(nextOrder);
};

const moveImage = (image, step) => {
  image.order = toNumberOrZero(image.order) + step;
};

const selectImageFromDb = (image, sourceId) => {
  const nextId = toNumberOrZero(sourceId);
  const source = activeGallerySource.value.find((item) => item.id === nextId);
  if (!source) return;

  releaseObjectUrl(image.localPreviewUrl);
  image.localPreviewUrl = null;
  image.localFile = null;
  image.localFileName = "";
  image.sourceType = "db";
  image.sourceImageId = source.id;
  image.alt_text = source.alt_text || "";
  image.image_webp_url = source.image_webp_url || source.image_url || "";
  image.image_placeholder_url = source.image_placeholder_url || null;
  image.image_url = source.image_url || source.image_webp_url || "";
};

const selectLocalImage = (image, event) => {
  const target = event?.target;
  const file = target?.files?.[0];
  if (!file || !import.meta.client) return;

  releaseObjectUrl(image.localPreviewUrl);
  const objectUrl = URL.createObjectURL(file);
  localObjectUrls.value.push(objectUrl);

  image.localPreviewUrl = objectUrl;
  image.localFile = file;
  image.localFileName = file.name;
  image.sourceType = "local";
  image.sourceImageId = null;
  target.value = "";
};

const resetGalleryPreview = () => {
  editableGalleryImages.value.forEach((item) => {
    releaseObjectUrl(item.localPreviewUrl);
  });
  editableGalleryImages.value = (galleryImages.value || [])
    .filter((item) => item?.position === "main" && item?.is_active)
    .map(createEditableGalleryItem);
};

const hasGalleryPreviewChanges = computed(() => {
  const sourceById = new Map((galleryImages.value || []).map((item) => [item.id, item]));
  return editableGalleryImages.value.some((item) => {
    const source = sourceById.get(item.id);
    if (!source) return false;
    return (
      toNumberOrZero(item.order) !== toNumberOrZero(source.order) ||
      item.sourceType === "local" ||
      toNumberOrZero(item.sourceImageId) !== toNumberOrZero(source.id)
    );
  });
});

const normalizeGalleryItems = (items) => {
  const normalized = [];
  ["left", "center", "right"].forEach((columnKey) => {
    const columnItems = sortByOrder(
      (items || []).filter((item) => (item?.column || "left") === columnKey)
    );
    columnItems.forEach((item, index) => {
      normalized.push({
        target_id: item.id,
        source_image_id: item.sourceImageId || item.id,
        position: "main",
        column: columnKey,
        order: index + 1,
        alt_text: item.alt_text || "",
        is_active: true,
      });
    });
  });
  return normalized;
};

const uploadLocalGalleryImages = async () => {
  for (const image of editableGalleryImages.value) {
    if (image.sourceType !== "local" || !image.localFile) continue;

    const formData = new FormData();
    formData.append("image", image.localFile);
    formData.append("alt_text", image.alt_text || "");
    formData.append("position", image.position || "main");
    formData.append("column", image.column || "left");
    formData.append("order", String(toNumberOrZero(image.order)));
    formData.append("is_active", "false");

    const uploaded = await postAdminContentForm("/auth/edit/gallery/upload/", formData);
    image.sourceType = "db";
    image.sourceImageId = uploaded?.id || null;
    image.alt_text = uploaded?.alt_text || image.alt_text || "";
    image.image_webp_url = uploaded?.image_webp_url || uploaded?.image_url || image.image_webp_url || "";
    image.image_placeholder_url = uploaded?.image_placeholder_url || null;
    image.image_url = uploaded?.image_url || uploaded?.image_webp_url || image.image_url || "";
  }
};

const saveGallery = async () => {
  if (!hasGalleryPreviewChanges.value || gallerySavePending.value) return;

  gallerySavePending.value = true;
  gallerySaveError.value = "";
  gallerySaveSuccess.value = "";

  try {
    await uploadLocalGalleryImages();

    const payloadItems = normalizeGalleryItems(editableGalleryImages.value);
    await postAdminContent("/auth/edit/gallery/apply/", { items: payloadItems });

    await Promise.all([refreshGalleryMain(), refreshGallerySource()]);
    resetGalleryPreview();
    gallerySaveSuccess.value = "Галерея сохранена";
  } catch (error) {
    gallerySaveError.value = error?.data?.detail || "Не удалось сохранить галерею";
  } finally {
    gallerySavePending.value = false;
  }
};

watch(
  () => props.editMode,
  async (enabled) => {
    if (!enabled) return;
    await refreshGallerySource();
  },
  { immediate: true }
);


let observer;

onMounted(() => {
  if (sectionRef.value) {
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          isVisible.value = true;
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(sectionRef.value);
  }
});

onBeforeUnmount(() => {
  editableGalleryImages.value.forEach((item) => {
    releaseObjectUrl(item.localPreviewUrl);
  });
  localObjectUrls.value.forEach((url) => {
    releaseObjectUrl(url);
  });
  if (observer) {
    observer.disconnect();
  }
});
</script>

<template>
  <section ref="sectionRef" class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div
        v-if="editMode"
        class="mb-4 inline-flex rounded-xl border border-primary/20 bg-muted px-3 py-2 text-xs font-medium text-primary"
      >
        Режим редактирования gallery/stats (превью)
      </div>

      <div class="mb-16">
        <div class="grid grid-cols-1 gap-3 md:grid-cols-3">
          <div class="flex flex-col gap-3">
            <div
              v-for="(image, index) in leftColumn"
              :key="`left-${image.id}`"
              class="transform overflow-hidden rounded-sm border border-border/50 transition-all duration-700"
              :class="
                isVisible
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-10'
              "
              :style="{
                transitionDelay: isVisible ? `${index * 150}ms` : '0ms',
              }"
            >
              <div class="relative h-[450px] overflow-hidden">
                <img
                  v-if="isLocalPreview(image)"
                  :src="getImageDisplaySrc(image)"
                  :alt="image.alt_text || 'Изображение галереи'"
                  class="h-full w-full object-cover"
                />
                <NuxtImg
                  v-else
                  :src="getImageDisplaySrc(image)"
                  :alt="image.alt_text || 'Изображение галереи'"
                  :width="414"
                  :height="552"
                  :placeholder="getImageDisplayPlaceholder(image)"
                  loading="lazy"
                  sizes="414px"
                  class="h-full w-full object-cover"
                />
              </div>
              <div
                v-if="editMode"
                class="border-t border-border/60 bg-card/90 p-2 text-xs text-foreground backdrop-blur"
              >
                <div class="mb-2 flex items-center gap-2">
                  <button
                    class="rounded-md border border-border px-2 py-1 hover:bg-muted"
                    @click="moveImage(image, -1)"
                  >
                    -1
                  </button>
                  <input
                    :value="image.order"
                    type="number"
                    class="w-20 rounded-md border border-border bg-background px-2 py-1"
                    @input="updateImageOrder(image, $event.target.value)"
                  />
                  <button
                    class="rounded-md border border-border px-2 py-1 hover:bg-muted"
                    @click="moveImage(image, 1)"
                  >
                    +1
                  </button>
                  <span class="text-[11px] text-muted-foreground">order</span>
                </div>
                <div class="space-y-2">
                  <div v-if="activeGallerySource.length" class="rounded-md border border-border/70 bg-background/80 p-2">
                    <div class="mb-2 flex items-center justify-between">
                      <p class="text-[11px] text-muted-foreground">Фото из БД</p>
                      <span class="text-[10px] text-muted-foreground">Выбрано: #{{ image.sourceImageId || "—" }}</span>
                    </div>
                    <div class="grid max-h-28 grid-cols-5 gap-1.5 overflow-y-auto pr-1">
                      <button
                        v-for="option in activeGallerySource"
                        :key="`left-preview-${image.id}-${option.id}`"
                        type="button"
                        class="group overflow-hidden rounded-md border transition-colors"
                        :class="isSourceSelected(image, option) ? 'border-primary ring-1 ring-primary/40' : 'border-border/70 hover:border-primary/60'"
                        @click="selectImageFromDb(image, option.id)"
                      >
                        <NuxtImg
                          :src="getSourcePreviewSrc(option)"
                          :alt="option.alt_text || `Фото #${option.id}`"
                          :width="96"
                          :height="72"
                          loading="lazy"
                          sizes="96px"
                          class="h-10 w-full object-cover"
                        />
                        <span class="block truncate border-t border-border/60 px-1 py-0.5 text-[10px] text-muted-foreground">
                          #{{ option.id }}
                        </span>
                      </button>
                    </div>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    class="w-full cursor-pointer rounded-md border border-dashed border-border bg-background px-2 py-1"
                    @change="selectLocalImage(image, $event)"
                  />
                  <p v-if="image.localFileName" class="text-[11px] text-muted-foreground">
                    Локальный файл: {{ image.localFileName }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <div
              v-for="(image, index) in centerColumn"
              :key="`center-${image.id}`"
              class="transform overflow-hidden rounded-sm border border-border/50 transition-all duration-700"
              :class="
                isVisible
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-10'
              "
              :style="{
                transitionDelay: isVisible ? `${(index + 2) * 150}ms` : '0ms',
              }"
            >
              <div class="relative h-[296px] overflow-hidden">
                <img
                  v-if="isLocalPreview(image)"
                  :src="getImageDisplaySrc(image)"
                  :alt="image.alt_text || 'Изображение галереи'"
                  class="h-full w-full object-cover"
                />
                <NuxtImg
                  v-else
                  :src="getImageDisplaySrc(image)"
                  :alt="image.alt_text || 'Изображение галереи'"
                  :width="414"
                  :height="296"
                  :placeholder="getImageDisplayPlaceholder(image)"
                  loading="lazy"
                  sizes="414px"
                  class="h-full w-full object-cover"
                />
              </div>
              <div
                v-if="editMode"
                class="border-t border-border/60 bg-card/90 p-2 text-xs text-foreground backdrop-blur"
              >
                <div class="mb-2 flex items-center gap-2">
                  <button
                    class="rounded-md border border-border px-2 py-1 hover:bg-muted"
                    @click="moveImage(image, -1)"
                  >
                    -1
                  </button>
                  <input
                    :value="image.order"
                    type="number"
                    class="w-20 rounded-md border border-border bg-background px-2 py-1"
                    @input="updateImageOrder(image, $event.target.value)"
                  />
                  <button
                    class="rounded-md border border-border px-2 py-1 hover:bg-muted"
                    @click="moveImage(image, 1)"
                  >
                    +1
                  </button>
                  <span class="text-[11px] text-muted-foreground">order</span>
                </div>
                <div class="space-y-2">
                  <div v-if="activeGallerySource.length" class="rounded-md border border-border/70 bg-background/80 p-2">
                    <div class="mb-2 flex items-center justify-between">
                      <p class="text-[11px] text-muted-foreground">Фото из БД</p>
                      <span class="text-[10px] text-muted-foreground">Выбрано: #{{ image.sourceImageId || "—" }}</span>
                    </div>
                    <div class="grid max-h-28 grid-cols-5 gap-1.5 overflow-y-auto pr-1">
                      <button
                        v-for="option in activeGallerySource"
                        :key="`center-preview-${image.id}-${option.id}`"
                        type="button"
                        class="group overflow-hidden rounded-md border transition-colors"
                        :class="isSourceSelected(image, option) ? 'border-primary ring-1 ring-primary/40' : 'border-border/70 hover:border-primary/60'"
                        @click="selectImageFromDb(image, option.id)"
                      >
                        <NuxtImg
                          :src="getSourcePreviewSrc(option)"
                          :alt="option.alt_text || `Фото #${option.id}`"
                          :width="96"
                          :height="72"
                          loading="lazy"
                          sizes="96px"
                          class="h-10 w-full object-cover"
                        />
                        <span class="block truncate border-t border-border/60 px-1 py-0.5 text-[10px] text-muted-foreground">
                          #{{ option.id }}
                        </span>
                      </button>
                    </div>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    class="w-full cursor-pointer rounded-md border border-dashed border-border bg-background px-2 py-1"
                    @change="selectLocalImage(image, $event)"
                  />
                  <p v-if="image.localFileName" class="text-[11px] text-muted-foreground">
                    Локальный файл: {{ image.localFileName }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <div
              v-for="(image, index) in rightColumn"
              :key="`right-${image.id}`"
              class="transform overflow-hidden rounded-sm border border-border/50 transition-all duration-700"
              :class="
                isVisible
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-10'
              "
              :style="{
                transitionDelay: isVisible ? `${(index + 5) * 150}ms` : '0ms',
              }"
            >
              <div class="relative h-[450px] overflow-hidden">
                <img
                  v-if="isLocalPreview(image)"
                  :src="getImageDisplaySrc(image)"
                  :alt="image.alt_text || 'Изображение галереи'"
                  class="h-full w-full object-cover"
                />
                <NuxtImg
                  v-else
                  :src="getImageDisplaySrc(image)"
                  :alt="image.alt_text || 'Изображение галереи'"
                  :width="414"
                  :height="552"
                  :placeholder="getImageDisplayPlaceholder(image)"
                  loading="lazy"
                  sizes="414px"
                  class="h-full w-full object-cover"
                />
              </div>
              <div
                v-if="editMode"
                class="border-t border-border/60 bg-card/90 p-2 text-xs text-foreground backdrop-blur"
              >
                <div class="mb-2 flex items-center gap-2">
                  <button
                    class="rounded-md border border-border px-2 py-1 hover:bg-muted"
                    @click="moveImage(image, -1)"
                  >
                    -1
                  </button>
                  <input
                    :value="image.order"
                    type="number"
                    class="w-20 rounded-md border border-border bg-background px-2 py-1"
                    @input="updateImageOrder(image, $event.target.value)"
                  />
                  <button
                    class="rounded-md border border-border px-2 py-1 hover:bg-muted"
                    @click="moveImage(image, 1)"
                  >
                    +1
                  </button>
                  <span class="text-[11px] text-muted-foreground">order</span>
                </div>
                <div class="space-y-2">
                  <div v-if="activeGallerySource.length" class="rounded-md border border-border/70 bg-background/80 p-2">
                    <div class="mb-2 flex items-center justify-between">
                      <p class="text-[11px] text-muted-foreground">Фото из БД</p>
                      <span class="text-[10px] text-muted-foreground">Выбрано: #{{ image.sourceImageId || "—" }}</span>
                    </div>
                    <div class="grid max-h-28 grid-cols-5 gap-1.5 overflow-y-auto pr-1">
                      <button
                        v-for="option in activeGallerySource"
                        :key="`right-preview-${image.id}-${option.id}`"
                        type="button"
                        class="group overflow-hidden rounded-md border transition-colors"
                        :class="isSourceSelected(image, option) ? 'border-primary ring-1 ring-primary/40' : 'border-border/70 hover:border-primary/60'"
                        @click="selectImageFromDb(image, option.id)"
                      >
                        <NuxtImg
                          :src="getSourcePreviewSrc(option)"
                          :alt="option.alt_text || `Фото #${option.id}`"
                          :width="96"
                          :height="72"
                          loading="lazy"
                          sizes="96px"
                          class="h-10 w-full object-cover"
                        />
                        <span class="block truncate border-t border-border/60 px-1 py-0.5 text-[10px] text-muted-foreground">
                          #{{ option.id }}
                        </span>
                      </button>
                    </div>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    class="w-full cursor-pointer rounded-md border border-dashed border-border bg-background px-2 py-1"
                    @change="selectLocalImage(image, $event)"
                  />
                  <p v-if="image.localFileName" class="text-[11px] text-muted-foreground">
                    Локальный файл: {{ image.localFileName }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="editMode" class="mt-4 flex flex-wrap items-center gap-2">
          <button
            class="rounded-lg px-3 py-2 text-xs font-semibold transition-colors"
            :class="
              hasGalleryPreviewChanges
                ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                : 'bg-muted text-muted-foreground'
            "
            :disabled="!hasGalleryPreviewChanges || gallerySavePending"
            @click="saveGallery"
          >
            {{ gallerySavePending ? "Сохранение..." : "Сохранить галерею" }}
          </button>
          <button
            class="rounded-lg border border-border px-3 py-2 text-xs font-semibold hover:bg-muted"
            @click="resetGalleryPreview"
          >
            Сбросить превью галереи
          </button>
          <span class="text-xs text-muted-foreground">
            {{ hasGalleryPreviewChanges ? "Есть изменения галереи" : "Изменений галереи пока нет" }}
          </span>
          <span v-if="gallerySaveSuccess" class="text-xs text-green-600">{{ gallerySaveSuccess }}</span>
          <span v-if="gallerySaveError" class="text-xs text-red-600">{{ gallerySaveError }}</span>
        </div>
      </div>

      <div
        class="mb-16 grid items-center gap-10 lg:grid-cols-[1.3fr_1fr]"
        :class="
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        "
        :style="{ transitionDelay: isVisible ? '400ms' : '0ms' }"
      >
        <div
          class="overflow-hidden rounded-2xl border border-border/50 bg-card/80 shadow-2xl backdrop-blur"
        >
          <div class="relative">
            <NuxtImg
              :src="basePlanImage"
              :width="694"
              :height="486"
              alt="План базы отдыха Строгановские Просторы"
              sizes="694px"
              class="h-auto w-full"
            />
            <div
              class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/10 to-transparent"
            />
          </div>
        </div>

        <div class="space-y-4">
          <h3 class="text-3xl font-serif text-primary md:text-4xl">
            {{ editablePlanTitle }}
          </h3>
          <p class="text-lg leading-relaxed text-muted-foreground">
            {{ editablePlanDescription1 }}
          </p>
          <p class="text-lg leading-relaxed text-muted-foreground">
            {{ editablePlanDescription2 }}
          </p>
          <div v-if="editMode" class="space-y-2 pt-2">
            <input
              v-model="editablePlanTitle"
              type="text"
              class="w-full rounded-xl border border-border bg-background p-3 text-sm text-foreground outline-none"
              placeholder="Заголовок блока"
            />
            <textarea
              v-model="editablePlanDescription1"
              rows="3"
              class="w-full rounded-xl border border-border bg-background p-3 text-sm text-foreground outline-none"
              placeholder="Первый абзац"
            />
            <textarea
              v-model="editablePlanDescription2"
              rows="4"
              class="w-full rounded-xl border border-border bg-background p-3 text-sm text-foreground outline-none"
              placeholder="Второй абзац"
            />
          </div>
        </div>
      </div>

      <div>
        <h3
          class="mb-10 text-center text-3xl font-serif text-primary transition-all duration-700 md:text-4xl"
          :class="
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          "
          :style="{ transitionDelay: isVisible ? '200ms' : '0ms' }"
        >
          Цифры и факты
        </h3>
        <div v-if="editMode" class="mx-auto mb-6 max-w-2xl text-center">
          <div class="mt-3 flex flex-wrap items-center justify-center gap-2">
            <button
              class="rounded-lg px-3 py-2 text-xs font-semibold transition-colors"
              :class="
                hasStatsChanges
                  ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                  : 'bg-muted text-muted-foreground'
              "
              :disabled="!hasStatsChanges || statsSavePending"
              @click="saveStatistics"
            >
              {{ statsSavePending ? "Сохранение..." : "Сохранить статистику" }}
            </button>
            <span v-if="statsSaveSuccess" class="text-xs text-green-600">{{ statsSaveSuccess }}</span>
            <span v-if="statsSaveError" class="text-xs text-red-600">{{ statsSaveError }}</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-5">
          <div
            v-for="(stat, index) in displayedStats"
            :key="stat?.id"
            class="group transform bg-[hsl(var(--stats-card))] p-6 text-center transition-all duration-700 rounded-2xl"
            :class="
              isVisible
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-10'
            "
            :style="{
              transitionDelay: isVisible ? `${200 + index * 80}ms` : '0ms',
            }"
          >
            <div class="space-y-2">
              <div
                class="text-4xl font-bold text-[hsl(var(--stats-card-foreground))] md:text-5xl"
              >
                {{ stat?.number }}
              </div>
              <div
                class="text-sm font-semibold text-[hsl(var(--stats-card-foreground)/0.9)] md:text-base"
              >
                {{ stat?.label }}
              </div>
              <div
                class="text-xs leading-relaxed text-[hsl(var(--stats-card-foreground)/0.7)]"
              >
                {{ stat?.description }}
              </div>
              <div v-if="editMode" class="space-y-2 pt-3 text-left">
                <input
                  v-model="editableStats[index].number"
                  type="text"
                  class="w-full rounded-lg border border-border/50 bg-background/95 p-2 text-xs text-foreground"
                  placeholder="Число"
                />
                <input
                  v-model="editableStats[index].label"
                  type="text"
                  class="w-full rounded-lg border border-border/50 bg-background/95 p-2 text-xs text-foreground"
                  placeholder="Подпись"
                />
                <textarea
                  v-model="editableStats[index].description"
                  rows="2"
                  class="w-full rounded-lg border border-border/50 bg-background/95 p-2 text-xs text-foreground"
                  placeholder="Описание"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- <div class="flex justify-center mt-10">
          <div style="width:360px;height:600px;overflow:hidden;position:relative;">
            <iframe
              style="width:100%;height:100%;border:1px solid #e6e6e6;border-radius:8px;box-sizing:border-box"
              src="https://yandex.ru/maps-reviews-widget/1277179994?comments"
            ></iframe>
            <a
              href="https://yandex.ru/maps/org/stroganovskiye_prostory/1277179994/"
              target="_blank"
              style="box-sizing:border-box;text-decoration:none;color:#b3b3b3;font-size:10px;font-family:YS Text,sans-serif;padding:0 20px;position:absolute;bottom:8px;width:100%;text-align:center;left:0;overflow:hidden;text-overflow:ellipsis;display:block;max-height:14px;white-space:nowrap;padding:0 16px;box-sizing:border-box"
            >Строгановские просторы на карте Пермского края — Яндекс Карты</a>
          </div>
        </div> -->
      </div>
    </div>
  </section>
</template>
