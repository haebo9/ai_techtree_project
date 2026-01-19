import { Edge, Node } from 'reactflow';
import { TechNodeData } from '@/types/techtree';

export const initialNodes: Node<TechNodeData>[] = [
    {
        id: 'python',
        type: 'techNode',
        position: { x: 250, y: 0 },
        data: {
            id: 'python',
            label: 'Python',
            description: 'The foundation of AI engineering. Master syntax and structures.',
            status: 'mastered',
            stars: 3,
            category: 'Language'
        },
    },
    {
        id: 'fastapi',
        type: 'techNode',
        position: { x: 100, y: 200 },
        data: {
            id: 'fastapi',
            label: 'FastAPI',
            description: 'High-performance web framework for building APIs.',
            status: 'available', // Changed to available (1 star usually means in progress or completed level 1, but let's say available for next level)
            stars: 1,
            category: 'Backend'
        },
    },
    {
        id: 'pandas',
        type: 'techNode',
        position: { x: 400, y: 200 },
        data: {
            id: 'pandas',
            label: 'Pandas',
            description: 'Data manipulation and analysis library.',
            status: 'available',
            stars: 0,
            category: 'Data'
        },
    },
    {
        id: 'docker',
        type: 'techNode',
        position: { x: 100, y: 400 },
        data: {
            id: 'docker',
            label: 'Docker',
            description: 'Containerization for consistent deployment.',
            status: 'locked',
            stars: 0,
            category: 'DevOps'
        },
    },
    {
        id: 'pytorch',
        type: 'techNode',
        position: { x: 400, y: 400 },
        data: {
            id: 'pytorch',
            label: 'PyTorch',
            description: 'Deep learning framework.',
            status: 'locked',
            stars: 0,
            category: 'AI'
        },
    },
];

export const initialEdges: Edge[] = [
    { id: 'e1-2', source: 'python', target: 'fastapi', animated: true },
    { id: 'e1-3', source: 'python', target: 'pandas', animated: true },
    { id: 'e2-4', source: 'fastapi', target: 'docker', style: { strokeOpacity: 0.3 } },
    { id: 'e3-5', source: 'pandas', target: 'pytorch', style: { strokeOpacity: 0.3 } },
];
