import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Star, Lock } from 'lucide-react';
import { TechNodeData } from '@/types/techtree';
import styles from './TechNode.module.css';

const TechNode = ({ data, selected }: NodeProps<TechNodeData>) => {
    const isLocked = data.status === 'locked';

    return (
        <div
            className={`
        ${styles.nodeWrapper} 
        ${styles[data.status]} 
        ${selected ? styles.selected : ''}
      `}
        >
            <Handle
                type="target"
                position={Position.Top}
                className={styles.handle}
            />

            <div className={styles.header}>
                <span className={styles.title}>{data.label}</span>
                {isLocked ? (
                    <Lock size={14} style={{ color: 'hsl(var(--color-text-muted))' }} />
                ) : (
                    <div className={styles.stars}>
                        {[1, 2, 3].map((star) => (
                            <Star
                                key={star}
                                size={12}
                                fill={star <= data.stars ? "currentColor" : "transparent"}
                                style={{
                                    color: star <= data.stars
                                        ? (data.status === 'mastered' ? 'hsl(var(--color-gold))' : 'hsl(var(--color-text-main))')
                                        : 'hsl(var(--color-text-muted))',
                                    opacity: star <= data.stars ? 1 : 0.3
                                }}
                            />
                        ))}
                    </div>
                )}
            </div>

            <p className={styles.description}>{data.description}</p>

            <Handle
                type="source"
                position={Position.Bottom}
                className={styles.handle}
            />
        </div>
    );
};

export default memo(TechNode);
