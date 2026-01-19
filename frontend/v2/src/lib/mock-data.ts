import { Edge, Node } from 'reactflow';
import { TechNodeData } from '@/types/techtree';

// Based on backend/app/source/tracks.json
// Track 0: Python -> Track 1: AI Engineer path

export const initialNodes: Node<TechNodeData>[] = [
    // --- Step 1: Programming Basics ---
    {
        id: 'python-syntax',
        type: 'techNode',
        position: { x: 250, y: 0 },
        data: {
            id: 'python-syntax',
            label: 'Python Syntax & Types',
            description: '변수, 제어문, 함수 등 Python의 가장 기초적인 문법 요소들입니다.',
            status: 'mastered',
            stars: 3,
            category: 'Language'
        },
    },
    {
        id: 'data-structure',
        type: 'techNode',
        position: { x: 100, y: 150 },
        data: {
            id: 'data-structure',
            label: 'Data Structure Core',
            description: 'List, Dictionary 등 데이터 관리를 위한 핵심 자료구조입니다.',
            status: 'mastered',
            stars: 3,
            category: 'CS'
        },
    },
    {
        id: 'oop-functional',
        type: 'techNode',
        position: { x: 400, y: 150 },
        data: {
            id: 'oop-functional',
            label: 'OOP & Functional',
            description: '객체지향(Class)과 함수형 프로그래밍의 기초 개념입니다.',
            status: 'available', // User is currently here
            stars: 1, // Level 1 completed
            category: 'Paradigm'
        },
    },

    // --- Step 2: Infrastructure Fundamentals ---
    {
        id: 'linux-cli',
        type: 'techNode',
        position: { x: 100, y: 350 },
        data: {
            id: 'linux-cli',
            label: 'Linux CLI',
            description: '마우스 없이 컴퓨터를 제어하는 명령어 기초입니다.',
            status: 'locked',
            stars: 0,
            category: 'OS'
        },
    },
    {
        id: 'git-vc',
        type: 'techNode',
        position: { x: 400, y: 350 },
        data: {
            id: 'git-vc',
            label: 'Git Version Control',
            description: '소스코드의 역사를 기록하고 협업하기 위한 도구입니다.',
            status: 'locked',
            stars: 0,
            category: 'Tool'
        },
    },

    // --- Track 1 Start ---
    {
        id: 'fastapi-essentials',
        type: 'techNode',
        position: { x: 100, y: 550 },
        data: {
            id: 'fastapi-essentials',
            label: 'FastAPI Essentials',
            description: 'Python 기반의 고성능 웹 프레임워크인 FastAPI의 핵심 기능을 익힙니다.',
            status: 'locked',
            stars: 0,
            category: 'Backend'
        },
    },
    {
        id: 'docker-basics',
        type: 'techNode',
        position: { x: 400, y: 550 },
        data: {
            id: 'docker-basics',
            label: 'Docker Basics',
            description: '어디서나 동일하게 실행되는 컨테이너 환경을 구축합니다.',
            status: 'locked',
            stars: 0,
            category: 'DevOps'
        },
    }
];

export const initialEdges: Edge[] = [
    // Python -> branches to Data Structure & OOP
    { id: 'e-py-ds', source: 'python-syntax', target: 'data-structure', animated: true },
    { id: 'e-py-oop', source: 'python-syntax', target: 'oop-functional', animated: true },

    // Foundation -> Infra (Logic: Need programming skills before system basics)
    { id: 'e-ds-linux', source: 'data-structure', target: 'linux-cli', style: { strokeOpacity: 0.2 } },
    { id: 'e-oop-git', source: 'oop-functional', target: 'git-vc', style: { strokeOpacity: 0.2 } },

    // Infra -> Backend (Logic: Need env setup before framework)
    { id: 'e-linux-docker', source: 'linux-cli', target: 'docker-basics', style: { strokeOpacity: 0.2 } },
    { id: 'e-git-fastapi', source: 'git-vc', target: 'fastapi-essentials', style: { strokeOpacity: 0.2 } },

    // Cross connections
    { id: 'e-linux-fastapi', source: 'linux-cli', target: 'fastapi-essentials', style: { strokeOpacity: 0.1 } },
];
