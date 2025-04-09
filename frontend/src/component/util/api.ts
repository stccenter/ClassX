export interface ImageMetadata {
    exposure_time: number;
    latitude: number;
    longitude: number;
    measurement: number;
    sun_distance: number;
    wavelength: number;
}

export interface ImageObject {
    alias: string;
    creation_date: string;
    crop_grid_path: string;
    file_type: string;
    h5_path: string;
    height: number;
    id: number;
    last_modified_date: string;
    metadata: ImageMetadata;
    mode: string;
    name: string;
    path: string;
    research_id: number;
    shared_by: string | null;
    shared_from: string | null;
    size: string;
    thumbnail_path: string;
    upload_time: string;
    user_id: number;
    visualization_path: string;
    width: number;
}

export interface CroppedImage {
    crop_size: number;
    crop_type: "man" | "auto";
    h5_path: string;
    height: number;
    id: number;
    last_modified_date: string;
    name: string;
    original_image_id: number;
    research_id: number;
    shared_by: string | null;
    shared_from: string | null;
    user_id: number;
    visualization_path: string;
    width: number;
}

