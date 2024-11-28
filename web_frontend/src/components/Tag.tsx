import React from 'react';
import { Tag as TagIcon } from 'lucide-react';
import { useTag } from '../contexts/TagContext';

interface TagProps {
  tag: string;
}

export function Tag({ tag }: TagProps) {
  const { selectedTag, setSelectedTag } = useTag();
  const isSelected = selectedTag === tag;

  return (
    <button
      onClick={() => setSelectedTag(isSelected ? null : tag)}
      className={`${
        isSelected
          ? 'bg-blue-600 text-white'
          : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
      } text-xs px-2 py-1 rounded-full flex items-center gap-1 transition-colors`}
    >
      <TagIcon size={12} />
      {tag}
    </button>
  );
}